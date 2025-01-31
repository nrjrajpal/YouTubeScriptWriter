from .researcher_agent import ResearcherAgent
from .synthetic_agent import SyntheticAgent
import yt_dlp
from utils.firebase import db
from datetime import datetime, timedelta
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
from flask import jsonify
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

class YouTubeAgent(ResearcherAgent):
    def __init__(self,  projectID, userEmail):
        super().__init__( projectID, userEmail)
        self.videoIDs = []  # Initialize video IDs as an empty list
        self.videoTranscripts = []  # Initialize video transcripts as an empty list (not stored in DB)

    # Video ID Functions
    def getVideoIDs(self):
        try: 
            if not self.videoIDs:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "videoIDs" not in record:
                    raise KeyNotFoundError("No video ids are present in the database.")

                self.videoIDs = record["videoIDs"]

            return self.videoIDs 
        except:
            raise

    def setVideoIDs(self, videoIDs):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"videoIDs": videoIDs})
            self.videoIDs = videoIDs
            
            return "Video IDs set successfully"
        except:
            raise
    
    def fetchVideoTranscript(self, videoID):
        # Simulate fetching a transcript for a given video ID
        # print(f"Fetching transcript for video ID: {videoID}")
        
        try:
            # Get available transcripts
            avail_lang = YouTubeTranscriptApi.list_transcripts(videoID)
            manual_langs = ['en'] + list(avail_lang._manually_created_transcripts)
            generated_langs = ['en'] + list(avail_lang._generated_transcripts)

        except TranscriptsDisabled:
            return "Transcript not available"

        transcript = None

        # Try to fetch manually created transcript
        for lang in manual_langs:
            try:
                transcript = avail_lang.find_manually_created_transcript([lang])
                # If the transcript is not in English, translate it
                if lang != 'en':
                    transcript = transcript.translate('en')
                break
            except (TranscriptsDisabled, NoTranscriptFound):
                continue

        # Fallback to auto-generated transcripts
        if not transcript:
            for lang in generated_langs:
                try:
                    transcript = avail_lang.find_generated_transcript([lang])
                    # If the transcript is not in English, translate it
                    if lang != 'en':
                        transcript = transcript.translate('en')
                    break
                except (TranscriptsDisabled, NoTranscriptFound):
                    continue

        # Fallback to native language transcript
        if not transcript:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(videoID)
            except (TranscriptsDisabled, NoTranscriptFound):
                return "Transcript not available"

        # Format the fetched transcript
        if transcript:
            # Extract transcript data
            transcript_data = transcript.fetch()
            formatter = TextFormatter()
            formatted_transcript = formatter.format_transcript(transcript_data)
            formatted_transcript=formatted_transcript.replace("\n", " ")

            if isinstance(formatted_transcript, str):
                return formatted_transcript
            else:
                return "Error formatting transcript"
        return "Transcript not available"


    # Video Metadata Fetching
    def fetchVideoMetadata(self, videoID):
        try:
            print(f"Fetching metadata for video ID: {videoID}")
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(videoID, download=False)
                metadata = {
                    'id': result['id'],
                    'title': result['title'],
                    'views': f"{(result['view_count'])}",
                    'duration': (result['duration']),
                    'publishedTime': datetime.strptime(result['upload_date'], "%Y%m%d").strftime("%B %d, %Y"),
                }
                
            formatted_count = self.format_count(metadata["views"])
            
            metadata["views"] = formatted_count + " views"
            metadata["duration"] = self.format_duration(metadata["duration"])
        except Exception as e:
            print(f"Error fetching metadata for {videoID}: {e}")
            # return jsonify({"message":"error"})
            return None
        
        return metadata
    
    # Fetch Videos From YouTube
    # The `fetchVideosFromYT` method in the `YouTubeAgent` class is responsible for fetching
    # videos from YouTube based on a search query. Here's a breakdown of what it does:
    def fetchVideosFromYT(self,max_results=3, min_duration=180, max_duration=18000):
        print(f"Fetching videos for search query: {self.searchQuery}")
        self.getSearchQuery()
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        
        filtered_video_ids = []
        unique_video_ids = set()
        fetched_videos = 0
        processed_videos = 0

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            while len(filtered_video_ids) < max_results and processed_videos < 30:
                result = ydl.extract_info(f"ytsearch{max_results + fetched_videos}:{self.searchQuery}", download=False)

                for video in result['entries']:
                    processed_videos += 1
                    video_id = video.get('id')
                    duration = video.get('duration', 0)
                    is_live = video.get('is_live', False)

                    # Ensure video meets criteria
                    if video_id not in unique_video_ids and min_duration <= duration <= max_duration and not is_live:
                        unique_video_ids.add(video_id)
                        filtered_video_ids.append(video_id)

                    if len(filtered_video_ids) >= max_results or processed_videos >= 30:
                        break

                fetched_videos += len(result['entries'])

        return filtered_video_ids
    
    @staticmethod
    def format_count(count):
        num = int(count)  # Convert count to integer
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B".rstrip('0').rstrip('.')
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M".rstrip('0').rstrip('.')
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K".rstrip('0').rstrip('.')
        else:
            return str(num)
        
    @staticmethod
    def format_duration(seconds):
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
