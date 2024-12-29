"use client";

import { useUser } from '@clerk/nextjs'
import { useParams, useRouter } from 'next/navigation'
import { useState, useCallback, useEffect, useRef } from "react";
import { Globe, FileText, Pencil, Check } from 'lucide-react';
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { Skeleton } from "@/components/ui/skeleton";

const YouTubeIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 22"
    fill="currentColor"
    className={className}
  >
    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
  </svg>
);

export default function DataInput() {
  const [openDialog, setOpenDialog] = useState<string | null>(null);
  const [inputValues, setInputValues] = useState<{ [key: string]: string[] }>({
    "YouTube Videos": ["", "", ""],
    "Web Pages": ["", "", ""],
    "Research Papers": ["", "", ""],
  });
  const [customText, setCustomText] = useState("");
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);
  const [manuallyDeselected, setManuallyDeselected] = useState<string[]>([]);
  const [hoverPosition, setHoverPosition] = useState<{
    x: number;
    y: number;
  } | null>(null);
  const [isHoveringButton, setIsHoveringButton] = useState(false);
  const { toast } = useToast();
  const params = useParams()
  const router = useRouter()

  const projectID = params.projectID as string
  const { isLoaded, isSignedIn, user } = useUser()

  const [originalYouTubeLinks, setOriginalYouTubeLinks] = useState<string[]>([]);
  const [latestValidYouTubeLinks, setLatestValidYouTubeLinks] = useState<string[]>([]);
  const [isLoadingYouTubeVideos, setIsLoadingYouTubeVideos] = useState(true);
  const [isDialogSubmitDisabled, setIsDialogSubmitDisabled] = useState(false);

  const [originalResearchPapers, setOriginalResearchPapers] = useState<any[]>([]);
  const [latestValidResearchPapers, setLatestValidResearchPapers] = useState<any[]>([]);
  const [isLoadingResearchPapers, setIsLoadingResearchPapers] = useState(true);

  const [originalWebPages, setOriginalWebPages] = useState<any[]>([]);
  const [latestValidWebPages, setLatestValidWebPages] = useState<any[]>([]);
  const [isLoadingWebPages, setIsLoadingWebPages] = useState(true);

  const [isGeneratingQuery, setIsGeneratingQuery] = useState(false);
  const [isComponentsDisabled, setIsComponentsDisabled] = useState(true);
  const [isInputInUse, setIsInputInUse] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const [isSearchQuerySet, setIsSearchQuerySet] = useState(false);

  const features = [
    {
      icon: YouTubeIcon,
      title: "YouTube Videos",
      color: "text-red-500",
      buttonText: "Add Custom Links",
      dialogTitle: "Add YouTube Video Links",
      subText:
        "Enter up to 3 YouTube video links. Current fields are filled with automatically fetched videos for the query.",
      points: [
        "Uses transcripts of YouTube videos",
        "Fetches English transcripts for script information",
        "Extracts diverse insights from video content"
      ],
    },
    {
      icon: Globe,
      title: "Web Pages",
      color: "text-blue-400",
      buttonText: "Add Custom Links",
      dialogTitle: "Add Web Page Links",
      subText:
        "Enter up to 3 web page URLs. Current fields are filled with automatically fetched webpages for the query.",
      points: [
        "Crawls web pages to gather detailed content",
        "Prioritizes reliable and relevant web sources"
      ],
    },
    {
      icon: FileText,
      title: "Research Papers",
      color: "text-green-400",
      buttonText: "Add Custom Links",
      dialogTitle: "Add Research Paper Links (Direct PDF Links)",
      subText:
        "Enter up to 3 direct PDF links. Current fields are filled with automatically fetched research paper links for the query.",
      points: [
        "Retrieves peer-reviewed research papers",
        "Extracts insights backed by data and evidence",
        "Focuses on high-quality academic sources"
      ],
    },
    {
      icon: Pencil,
      title: "Custom",
      color: "text-amber-400",
      buttonText: "Add Custom Text",
      dialogTitle: "Add Custom Information",
      subText:
        "Enter your custom information below. Maximum 20,000 characters.",
      points: [
        "Information tailored to your needs",
        "Allows unique, unseen ideas to be used",
        "Ensures flexibility for custom material"
      ],
    },
  ];

  const handleSubmit = useCallback(
    (title: string) => {
      if (title === "YouTube Videos") {
        const updatedLinks = inputValues[title].map((link, index) => {
          if (link.startsWith("https://www.youtube.com/watch?v=")) {
            return link;
          } else {
            return latestValidYouTubeLinks[index] || originalYouTubeLinks[index] || "";
          }
        });
        setInputValues(prev => ({
          ...prev,
          [title]: updatedLinks
        }));
      } else if (title === "Research Papers") {
        const updatedLinks = inputValues[title].map((link, index) => {
          if (link.startsWith("http")) {
            return link;
          } else {
            return latestValidResearchPapers[index]?.paper_url || originalResearchPapers[index]?.paper_url || "";
          }
        });
        setInputValues(prev => ({
          ...prev,
          [title]: updatedLinks
        }));
      } else if (title === "Web Pages") {
        const updatedLinks = inputValues[title].map((link, index) => {
          if (link.startsWith("http")) {
            return link;
          } else {
            return latestValidWebPages[index]?.webpage_url || originalWebPages[index]?.webpage_url || "";
          }
        });
        setInputValues(prev => ({
          ...prev,
          [title]: updatedLinks
        }));
      } else if (title === "Custom") {
        console.log(`Submitted for ${title}:`, customText);
      } else {
        console.log(`Submitted for ${title}:`, inputValues[title]);
      }
      setOpenDialog(null);
    },
    [inputValues, latestValidYouTubeLinks, originalYouTubeLinks, latestValidResearchPapers, originalResearchPapers, latestValidWebPages, originalWebPages, customText]
  );

  const handleInputChange = useCallback(
    (title: string, index: number, value: string) => {
      setInputValues((prev) => ({
        ...prev,
        [title]: prev[title].map((v, i) => (i === index ? value : v)),
      }));

      if (title === "YouTube Videos") {
        const isValidYouTubeLink = value.startsWith("https://www.youtube.com/watch?v=");
        setIsDialogSubmitDisabled(!isValidYouTubeLink);
        if (isValidYouTubeLink) {
          setLatestValidYouTubeLinks((prev) => {
            const newLinks = [...prev];
            newLinks[index] = value;
            return newLinks;
          });
        }
      } else if (title === "Research Papers" || title === "Web Pages") {
        const isValidLink = value.startsWith("http");
        if (isValidLink) {
          if (title === "Research Papers") {
            setLatestValidResearchPapers((prev) => {
              const newPapers = [...prev];
              newPapers[index] = { paper_url: value, paper_title: value };
              return newPapers;
            });
          } else {
            setLatestValidWebPages((prev) => {
              const newPages = [...prev];
              newPages[index] = { webpage_url: value, webpage_title: value, webpage_raw_content: "" };
              return newPages;
            });
          }
        }
      }

      if (value.trim() !== "") {
        setSelectedFeatures((prev) =>
          prev.includes(title) ? prev : [...prev, title]
        );
        setManuallyDeselected((prev) => prev.filter((item) => item !== title));
      } else if (
        inputValues[title].every((v, i) => i === index || v.trim() === "")
      ) {
        setSelectedFeatures((prev) => prev.filter((item) => item !== title));
      }
    },
    [inputValues]
  );

  const handleCustomTextChange = useCallback((value: string) => {
    setCustomText(value);
    if (value.trim() !== "") {
      setSelectedFeatures((prev) =>
        prev.includes("Custom") ? prev : [...prev, "Custom"]
      );
      setManuallyDeselected((prev) => prev.filter((item) => item !== "Custom"));
    } else {
      setSelectedFeatures((prev) => prev.filter((item) => item !== "Custom"));
    }
  }, []);

  const [searchQuery, setSearchQuery] = useState("");
  const searchQueryRef = useRef("");

  const generateSearchQuery = useCallback(async () => {
    setIsGeneratingQuery(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/generateSearchQuery`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userEmail: user?.primaryEmailAddress?.emailAddress,
          projectID: projectID
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        setSearchQuery(data.searchQuery);
        searchQueryRef.current = data.searchQuery;
      } else {
        throw new Error(data.error || "Failed to generate search query");
      }
    } catch (error) {
      console.error("Error generating search query:", error);
      toast({
        title: "Error",
        description: "Failed to generate search query. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsGeneratingQuery(false);
    }
  }, [user, projectID, toast]);

  const setSearchQueryAPI = useCallback(async (query: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setSearchQuery`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userEmail: user?.primaryEmailAddress?.emailAddress,
          projectID: projectID,
          searchQuery: query
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (!data.success) {
        throw new Error(data.error || "Failed to set search query");
      }
    } catch (error) {
      console.error("Error setting search query:", error);
      toast({
        title: "Error",
        description: "Failed to set search query. Please try again.",
        variant: "destructive",
      });
    }
  }, [user, projectID, toast]);

  const handleSearchSubmit = async () => {
    setIsGeneratingQuery(true);
    try {
      await setSearchQueryAPI(searchQuery);
      setIsSearchQuerySet(true);
      setIsComponentsDisabled(false);
      await Promise.all([
        fetchVideosFromYT(),
        fetchResearchPaperFromWeb(),
        fetchWebPagesFromWeb()
      ]);
    } catch (error) {
      console.error("Error submitting search query:", error);
      toast({
        title: "Error",
        description: "Failed to submit search query. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsGeneratingQuery(false);
    }
  };

  const handleSearchInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    setIsSearchQuerySet(false);
  };

  const fetchVideosFromYT = useCallback(async () => {
    setIsLoadingYouTubeVideos(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/fetchVideosFromYT`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userEmail: user?.primaryEmailAddress?.emailAddress,
          projectID: projectID
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        const videoUrls = data.video_urls.slice(0, 3);
        setInputValues(prev => ({
          ...prev,
          "YouTube Videos": videoUrls
        }));
        setOriginalYouTubeLinks(videoUrls);
        setLatestValidYouTubeLinks(videoUrls);
      } else {
        throw new Error(data.error || "Failed to fetch YouTube videos");
      }
    } catch (error) {
      console.error("Error fetching YouTube videos:", error);
      toast({
        title: "Error",
        description: "Failed to fetch YouTube videos. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoadingYouTubeVideos(false);
    }
  }, [user, projectID, toast, setInputValues]);

  const fetchResearchPaperFromWeb = useCallback(async () => {
    setIsLoadingResearchPapers(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/fetchResearchPaperFromWeb`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userEmail: user?.primaryEmailAddress?.emailAddress,
          projectID: projectID
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        const papers = data["research papers"].slice(0, 3);
        setInputValues(prev => ({
          ...prev,
          "Research Papers": papers.map((paper: any) => paper.paper_url)
        }));
        setOriginalResearchPapers(papers);
        setLatestValidResearchPapers(papers);
      } else {
        throw new Error(data.error || "Failed to fetch research papers");
      }
    } catch (error) {
      console.error("Error fetching research papers:", error);
      toast({
        title: "Error",
        description: "Failed to fetch research papers. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoadingResearchPapers(false);
    }
  }, [user, projectID, toast, setInputValues]);

  const fetchWebPagesFromWeb = useCallback(async () => {
    setIsLoadingWebPages(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/fetchWebPagesFromWeb`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userEmail: user?.primaryEmailAddress?.emailAddress,
          projectID: projectID
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        const webpages = data["webpage content"].slice(0, 3);
        setInputValues(prev => ({
          ...prev,
          "Web Pages": webpages.map((webpage: any) => webpage.webpage_url)
        }));
        setOriginalWebPages(webpages);
        setLatestValidWebPages(webpages);
      } else {
        throw new Error(data.error || "Failed to fetch web pages");
      }
    } catch (error) {
      console.error("Error fetching web pages:", error);
      toast({
        title: "Error",
        description: "Failed to fetch web pages. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoadingWebPages(false);
    }
  }, [user, projectID, toast, setInputValues]);

  const handleMainSubmit = useCallback(async () => {
    if (selectedFeatures.length === 0) {
      toast({
        title: "No sources selected",
        description:
          "Please select at least one information source before submitting.",
        variant: "destructive",
      });
      return;
    }

    const selectedData: any = {};
    selectedFeatures.forEach(feature => {
      if (feature === "Custom") {
        selectedData[feature] = customText;
      } else {
        selectedData[feature] = inputValues[feature];
      }
    });

    console.log("Selected data:", selectedData);

    const payload = {
      "YouTube Videos_selected": selectedFeatures.includes("YouTube Videos"),
      "YouTube Videos_links": selectedFeatures.includes("YouTube Videos") ? inputValues["YouTube Videos"].filter(
        (link) => link.trim() !== ""
      ) : [],
      "Web Pages_selected": selectedFeatures.includes("Web Pages"),
      "Web Pages_links": selectedFeatures.includes("Web Pages") ? inputValues["Web Pages"].filter(
        (link) => link.trim() !== ""
      ) : [],
      "Research Papers_selected": selectedFeatures.includes("Research Papers"),
      "Research Papers_links": selectedFeatures.includes("Research Papers") ? inputValues["Research Papers"].filter(
        (link) => link.trim() !== ""
      ) : [],
      Custom_selected: selectedFeatures.includes("Custom"),
      Custom_text: selectedFeatures.includes("Custom") ? customText : "",
      userEmail: user?.primaryEmailAddress?.emailAddress,
      projectID: projectID
    };

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/submitSources`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("API response:", data);

      if (selectedFeatures.includes("YouTube Videos")) {
        const videoIDsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setVideoIDs`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userEmail: user?.primaryEmailAddress?.emailAddress,
            projectID: projectID,
            video_urls: inputValues["YouTube Videos"]
          }),
        });

        if (!videoIDsResponse.ok) {
          throw new Error(`HTTP error! status: ${videoIDsResponse.status}`);
        }

        const videoIDsData = await videoIDsResponse.json();
        console.log("setVideoIDs API response:", videoIDsData);
      }

      if (selectedFeatures.includes("Research Papers")) {
        const researchPaperData = inputValues["Research Papers"].map((url, index) => {
          const originalPaper = originalResearchPapers[index];
          return {
            paper_url: url,
            paper_title: url !== originalPaper.paper_url ? url : originalPaper.paper_title,
          };
        });

        const researchPaperResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setResearchPaperData`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userEmail: user?.primaryEmailAddress?.emailAddress,
            projectID: projectID,
            researchPaperData: researchPaperData
          }),
        });

        if (!researchPaperResponse.ok) {
          throw new Error(`HTTP error! status: ${researchPaperResponse.status}`);
        }

        const researchPaperResult = await researchPaperResponse.json();
        console.log("setResearchPaperData API response:", researchPaperResult);
      }

      if (selectedFeatures.includes("Web Pages")) {
        const webPageData = inputValues["Web Pages"].map((url, index) => {
          const originalWebPage = originalWebPages[index];
          return {
            webpage_url: url,
            webpage_title: url !== originalWebPage.webpage_url ? url : originalWebPage.webpage_title,
            webpage_raw_content: url !== originalWebPage.webpage_url ? "N/A" : originalWebPage.webpage_raw_content,
          };
        });

        const webPageResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setWebPageData`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userEmail: user?.primaryEmailAddress?.emailAddress,
            projectID: projectID,
            webPageData: webPageData
          }),
        });

        if (!webPageResponse.ok) {
          throw new Error(`HTTP error! status: ${webPageResponse.status}`);
        }

        const webPageResult = await webPageResponse.json();
        console.log("setWebPageData API response:", webPageResult);
      }

      if (selectedFeatures.includes("Custom")) {
        const customDataResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setCustomData`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userEmail: user?.primaryEmailAddress?.emailAddress,
            projectID: projectID,
            customData: customText
          }),
        });

        if (!customDataResponse.ok) {
          throw new Error(`HTTP error! status: ${customDataResponse.status}`);
        }

        const customDataResult = await customDataResponse.json();
        console.log("setCustomData API response:", customDataResult);
      }

      toast({
        title: "Success",
        description: "Data submitted successfully",
      });

      router.push(`/project/selectQuestions/${projectID}`);

    } catch (error) {
      console.error("Error submitting data:", error);
      toast({
        title: "Error",
        description:
          "An error occurred while submitting the data. Please try again.",
        variant: "destructive",
      });
    }
  }, [inputValues, customText, selectedFeatures, toast, router, projectID, user, originalResearchPapers, originalWebPages]);

  const toggleFeatureSelection = useCallback((title: string) => {
    setSelectedFeatures((prev) => {
      if (prev.includes(title)) {
        setManuallyDeselected((md) => [...md, title]);
        return prev.filter((t) => t !== title);
      } else {
        setManuallyDeselected((md) => md.filter((t) => t !== title));
        return [...prev, title];
      }
    });
  }, []);

  useEffect(() => {
    setSelectedFeatures((prev) => {
      const newSelectedFeatures = features
        .filter((feature) => {
          if (manuallyDeselected.includes(feature.title)) {
            return false;
          }
          if (feature.title === "Custom") {
            return customText.trim() !== "";
          } else {
            return inputValues[feature.title].some(
              (value) => value.trim() !== ""
            );
          }
        })
        .map((feature) => feature.title);

      return [...new Set([...prev, ...newSelectedFeatures])];
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inputValues, customText, manuallyDeselected]);

  useEffect(() => {
    const fetchData = async () => {
      if (user?.primaryEmailAddress?.emailAddress && projectID) {
        await generateSearchQuery();
        setIsSearchQuerySet(false);
      }
    };

    fetchData();
  }, [user, projectID, generateSearchQuery]);

  const ToggleButton = ({ title }: { title: string }) => (
    <button
      className={`absolute top-2 right-2 w-6 h-6 flex items-center justify-center rounded-2xl transition-colors ${
        selectedFeatures.includes(title)
          ? "bg-green-500 text-white"
          : "bg-transparent"
      }`}
      onClick={(e) => {
        e.stopPropagation();
        toggleFeatureSelection(title);
      }}
    >
      {selectedFeatures.includes(title) && <Check className="w-4 h-4" />}
    </button>
  );

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isHoveringButton) {
      setHoverPosition({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseLeave = () => {
    setHoverPosition(null);
  };

  return (
    <div className="flex items-center justify-center flex-col min-h-screen p-4 sm:p-6 lg:p-8 text-base sm:text-lg">
      <div className="rounded-2xl w-full max-w-[1380px] sm:w-5/6 lg:w-4/5 xl:w-3/4 h-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
        <div className="bg-black rounded-2xl justify-center items-center py-4 px-4">
          <h1 className="pt-5 text-4xl font-medium font-script text-center">
            Select Information Sources
          </h1>
          <div className="pt-10 flex w-full max-w-sm items-center space-x-2 mb-4 mx-auto">
            <Input
              type="text"
              placeholder="Search query"
              value={searchQuery}
              onChange={handleSearchInputChange}
              disabled={isGeneratingQuery || isSearchQuerySet}
              ref={searchInputRef}
              className="p-2 text-md h-12 border bg-gray-900 border-gray-600 rounded-lg focus:ring-blue-500 "
            />
            <Button 
              type="submit" 
              disabled={isGeneratingQuery || !searchQuery || isSearchQuerySet} 
              onClick={handleSearchSubmit}
              className="border border-gray-600 text-md h-12 w-auto px-6 rounded-lg bg-gray-900 text-white hover:bg-gray-800 font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Set Query
            </Button>
          </div>
          <p className="text-center text-sm text-gray-400 mb-4">
            After setting the search query, click to select or deselect a source. Sources with content will be
            automatically selected, <br/>but you can unselect them.
          </p>
          <div className={`grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 sm:gap-6 lg:gap-8 ${!isSearchQuerySet ? 'opacity-50 pointer-events-none' : ''}`}>
            {features.map((feature, index) => (
              <div
                key={index}
                className={`bg-gray-900 rounded-2xl px-6 sm:px-6 lg:px-8 pb-6 sm:pb-6 lg:pb-8 pt-4 sm:pt-4 lg:pt-6 flex flex-col relative cursor-pointer ${
                  selectedFeatures.includes(feature.title)
                    ? "ring-2 ring-green-500"
                    : ""
                }`}
                onClick={() => toggleFeatureSelection(feature.title)}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
              >
                <ToggleButton title={feature.title} />
                <div className="flex items-center mb-3 sm:mb-4">
                  <feature.icon
                    className={`w-7 h-7 mr-3 sm:mr-4 ${feature.color}`}
                  />
                  <h2 className="font-script text-lg sm:text-2xl font-semibold text-white">
                    {feature.title}
                  </h2>
                </div>
                <ul className="font-script font-medium list-disc list-inside space-y-1 sm:space-y-1 text-gray-300 flex-grow text-sm">
                  {feature.points.map((point, pointIndex) => (
                    <li key={pointIndex}>{point}</li>
                  ))}
                </ul>
                {((feature.title === "YouTube Videos" && isLoadingYouTubeVideos) ||
                (feature.title === "Research Papers" && isLoadingResearchPapers) ||
                (feature.title === "Web Pages" && isLoadingWebPages)) ? (
                  <div className="space-y-2">
                    <br/>
                    <Skeleton className="h-4 w-[200px]" />
                    <Skeleton className="h-4 w-[280px]" />
                  </div>
                ) : (
                  <Dialog
                    open={openDialog === feature.title}
                    onOpenChange={(open) => {
                      setOpenDialog(open ? feature.title : null);
                      if (!open) {
                        handleSubmit(feature.title);
                      }
                    }}
                  >
                    <DialogTrigger asChild>
                      <Button
                        variant="default"
                        className="rounded-2xl bg-gray-950 text-white mt-4 sm:mt-6 text-sm sm:text-base lg:text-lg hover:bg-indigo-950 transition-all border-gray-700 border-2 py-4 sm:py-6"
                        onClick={(e) => {
                          e.stopPropagation();
                          setOpenDialog(feature.title);
                        }}
                        onMouseEnter={() => setIsHoveringButton(true)}
                        onMouseLeave={() => setIsHoveringButton(false)}
                      >
                        {feature.buttonText}
                      </Button>
                    </DialogTrigger>
                    <DialogContent
                      className="sm:max-w-[50vw] md:max-w-[450px] bg-gray-950 text-white border border-gray-800 w-11/12 p-4 sm:p-6 lg:p-8 rounded-xl"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <DialogHeader>
                        <DialogTitle className="font-script text-xl sm:text-2xl lg:text-2xl">
                          {feature.dialogTitle}
                        </DialogTitle>
                      </DialogHeader>
                      <p className="font-script text-sm text-gray-400 mb-2">
                        {feature.subText}
                      </p>
                      {feature.title === "YouTube Videos" && (
                        <p className="font-script text-sm text-gray-400 mb-2">
                          Example of a valid URL format: <br/> https://www.youtube.com/watch?v= &lt;desired youtube video's ID&gt;
                        </p>
                      )}
                      <div className="font-script grid gap-3 sm:gap-4 py-3 sm:py-4">
                        {feature.title === "Custom" ? (
                          <Textarea
                            placeholder="Enter your custom information here"
                            value={customText}
                            onChange={(e) =>
                              handleCustomTextChange(e.target.value)
                            }
                            maxLength={20000}
                            className="font-script h-40 sm:h-60 bg-gray-900 text-white text-sm sm:text-lg lg:text-lg p-3 sm:p-4"
                          />
                        ) : (
                          inputValues[feature.title].map((value, i) => (
                            <Input
                              key={i}
                              placeholder={`Link ${i + 1}`}
                              value={value}
                              onChange={(e) =>
                                handleInputChange(
                                  feature.title,
                                  i,
                                  e.target.value
                                )
                              }
                              className="font-script bg-gray-900 text-white text-sm h-12 w-full"
                            />
                          ))
                        )}
                      </div>
                      <Button
                        onClick={() => handleSubmit(feature.title)}
                        variant="default"
                        className="font-script border border-gray-700 rounded-2xl bg-gray-900 text-white hover:bg-slate-800 transition-all hover:border-[3px] w-full text-base sm:text-lg lg:text-xl h-10 sm:h-12  lg:h-14"
                        disabled={feature.title === "YouTube Videos" && isDialogSubmitDisabled}
                      >
                        Submit
                      </Button>
                    </DialogContent>
                  </Dialog>
                )}
              </div>
            ))}
          </div>
          <div className="my-4 relative group flex w-full sm:w-[80%] md:w-[70%] lg:w-[600px] justify-center mx-auto">
          <div className="h-fit relative group flex w-full justify-center mx-auto">
            <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                  <Button onClick={handleMainSubmit} disabled={!isSearchQuerySet} type="submit" variant={"gradient"} className={`font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium`}>
                    Submit
                  </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
      {hoverPosition && !isHoveringButton && (
        <div
          className="fixed pointer-events-none z-50 bg-gray-800 text-white px-2 py-1 rounded-md text-sm"
          style={{
            left: `${hoverPosition.x + 10}px`,
            top: `${hoverPosition.y + 10}px`,
          }}
        >
          Click to select
        </div>
      )}
    </div>
  );
}

