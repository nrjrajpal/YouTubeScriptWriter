"use client";

import { useState, useEffect } from "react";
import React from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useUser } from '@clerk/nextjs'
import { useParams, useRouter } from 'next/navigation'
import { Lightbulb, MessageSquare, Globe, FileText, Pencil } from 'lucide-react';
import { Skeleton } from "@/components/ui/skeleton";
import Image from "next/image";
import { useState as useState2 } from "react"; // Added import


interface VideoDetails {
  id: string;
  title: string;
  views: string;
  duration: string;
  publishedTime: string;
}

interface AccordionData {
  ideaDetails: {
    title: string;
    description: string;
  } | null;
  selectedQuestions: string[] | null;
  youtubeVideos: {
    available: boolean;
    data?: VideoDetails[];
    message?: string;
  } | null;
  webpages: {
    available: boolean;
    data?: { title: string; url: string }[];
    message?: string;
  } | null;
  researchPapers: {
    available: boolean;
    data?: { title: string; authors: string; url: string }[];
    message?: string;
  } | null;
  customData: {
    available: boolean;
    data?: string;
    message?: string;
  } | null;
}

interface ThoughtProcessParagraph {
  paragraph: string;
  color: string;
}

const API_BASE_URL = `${process.env.NEXT_PUBLIC_API_BASE_URL}/`;

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

export default function Component() {
  const { isLoaded, isSignedIn, user } = useUser()
  const router = useRouter()

  const params = useParams();
  const projectID = params.projectID as string;
  
  const [payload, setPayload] = useState<{userEmail: string | null; projectID: string; } | null> (null);
  const [viewMode, setViewMode] = useState<"thought" | "script">("thought");
  const [loading, setLoading] = useState({
    projectTitle: true,
    ideaDetails: true,
    selectedQuestions: true,
    youtubeVideos: true,
    webpages: true,
    researchPapers: true,
    customData: true,
    thoughtProcess: true,
    finalScript: true,
  });
  const [projectTitle, setProjectTitle] = useState<string>("");
  const [accordionData, setAccordionData] = useState<AccordionData>({
    ideaDetails: null,
    selectedQuestions: null,
    youtubeVideos: null,
    webpages: null,
    researchPapers: null,
    customData: null,
  });
  const [thoughtProcess, setThoughtProcess] = useState<ThoughtProcessParagraph[]> ([]);
  // const [isThoughtProcessDataLoaded, setIsThoughtProcessDataLoaded] = useState(false); 
  // const [finalScript, setFinalScript] = useState<string>("");
  const [expandedAccordions, setExpandedAccordions] = useState<{ [key: string]: boolean }>({}); // Added state


  const fetchData = async (endpoint: string, key: keyof typeof loading) => {
    if (!isLoaded || !isSignedIn || !projectID) {
      return
    }
    const payload = {
      userEmail: user?.primaryEmailAddress?.emailAddress,
      projectID: projectID
    }
    try {
      if (key === "thoughtProcess") {
        console.log(projectID)
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
        const reader = response.body?.getReader();
        const decoder = new TextDecoder("utf-8");
        let previousText = "";

        if (reader) {
          setLoading((prev) => ({ ...prev, [key]: false }));
          let done = false;

          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;

            const chunk = decoder.decode(value, { stream: true });
            const combinedText = previousText + chunk;

            const splitParagraphs = combinedText.split("\n\n");
            previousText = splitParagraphs.pop() || "";

            const newParagraphs = splitParagraphs
              .filter((p) => p.trim() !== "")
              .map((p) => {
                try {
                  const parsed = JSON.parse(p.replace(/^data: /, ""));
                  // console.log(parsed.paragraph)
                  return parsed as ThoughtProcessParagraph;
                  // eslint-disable-next-line @typescript-eslint/no-unused-vars
                } catch (e) {
                  return { paragraph: p, color: "text-white" };
                }
              });

            setThoughtProcess((prev) => [...prev, ...newParagraphs]);
          }

          if (previousText.trim()) {
            try {
              const parsed = JSON.parse(previousText.replace(/^data: /, ""));
              setThoughtProcess((prev) => [
                ...prev,
                parsed as ThoughtProcessParagraph,
              ]);
              // eslint-disable-next-line @typescript-eslint/no-unused-vars
            } catch (e) {
              setThoughtProcess((prev) => [
                ...prev,
                { paragraph: previousText, color: "text-white" },
              ]);
            }
          }
        }
        // setIsThoughtProcessDataLoaded(true);
      } else {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (key === "projectTitle") {
          setProjectTitle(data.title);
        } else if (key === "finalScript") {
          // setFinalScript(data);
        } else {
          setAccordionData((prev) => ({ ...prev, [key]: data }));
        }
        setLoading((prev) => ({ ...prev, [key]: false }));
      }
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      setLoading((prev) => ({ ...prev, [key]: false }));
    }
  };


  useEffect(() => {
    // router.refresh();
    fetchData("getVideoTitle", "projectTitle");
    fetchData("getIdeaDetails", "ideaDetails");
    fetchData("getSelectedQuestions", "selectedQuestions");
    fetchData("getYoutubeVideos", "youtubeVideos");
    fetchData("getWebPages", "webpages");
    fetchData("getResearchPapers", "researchPapers");
    fetchData("getCustomData", "customData");
    fetchData("getThoughtProcess", "thoughtProcess");     // scrit is generated in thought process
    // fetchData("getFinalScript", "finalScript");
  }, [isLoaded, isSignedIn, user, projectID]);

  // useEffect(() => {
  //   if (thoughtProcess.length > 0 && isThoughtProcessDataLoaded) {
  //     console.log("Thought process fully loaded");
  //     fetchData("getFinalScript", "finalScript");
  //   }
  // }, [thoughtProcess, isThoughtProcessDataLoaded]);

  const getVisibleColorClass = (color: string) => {
    const colorMap: { [key: string]: string } = {
      "text-blue-500": "text-blue-300",
      "text-green-500": "text-green-300",
      "text-red-500": "text-red-300",
      "text-purple-500": "text-purple-300",
      "text-yellow-500": "text-yellow-300",
    };
    return colorMap[color] || color;
  };

  const renderAccordionContent = (content: React.ReactNode, accordionId: string) => {
    const paragraphs = React.Children.toArray(content);
    const isExpanded = expandedAccordions[accordionId];
    
    let visibleContent;
    if (accordionId === "final-script") {
      const scriptContent = (paragraphs[0] as React.ReactElement).props.children;
      visibleContent = isExpanded ? scriptContent : scriptContent.slice(0, 300);
    } else {
      visibleContent = isExpanded ? paragraphs : [paragraphs[0]];
    }

    return (
      <>
        {visibleContent}
        {((accordionId === "final-script" && (paragraphs[0] as React.ReactElement).props.children.length > 300) || 
           (accordionId !== "final-script" && paragraphs.length > 1)) && !isExpanded && (
          <div className="relative">
            <div className="absolute bottom-0 left-0 w-full h-20 bg-gradient-to-t from-black to-transparent"></div>
            <Button
              onClick={() => setExpandedAccordions(prev => ({ ...prev, [accordionId]: true }))}
              className="border absolute bottom-0 left-1/2 transform -translate-x-1/2 z-10 bg-gray-900 text-white hover:bg-gray-700"
            >
              Load More
            </Button>
          </div>
        )}
      </>
    );
  };

  return (
    <div className="min-h-screen bg-black text-white p-4 sm:p-6 flex flex-col overflow-hidden">
      <style jsx global>{`
        ::-webkit-scrollbar {
          width: 10px;
        }
        ::-webkit-scrollbar-track {
          background: #2d3748;
        }
        ::-webkit-scrollbar-thumb {
          background: #4a5568;
          border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: #718096;
        }
      `}</style>
      {loading.projectTitle ? (
        <Skeleton className="h-8 sm:h-10 w-3/4 mx-auto mb-4 sm:mb-8" />
      ) : (
        <h1 className="text-xl sm:text-2xl font-medium mb-4 sm:mb-8 text-center font-script">
          Video Title: {projectTitle}
        </h1>
      )}

      <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 flex-grow h-full lg:h-full overflow-hidden">
        <div className=" flex rounded-2xl w-full lg:w-1/2 bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg overflow-hidden">
          <div className="w-full h-full bg-black rounded-2xl py-4 px-2 sm:px-4 overflow-hidden p-4 sm:p-6">
            <h2 className="mt-2 text-xl font-script sm:text-2xl text-center font-medium">
              Details
            </h2>
            <div className="overflow-y-auto flex-grow w-full pr-2 sm:pr-4">
              <Accordion type="multiple" className="w-full py-[17]">
                <AccordionItem value="item-0">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <Lightbulb className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-yellow-400 " />
                      <span className="text-sm font-script sm:text-[15px]" >Idea Details</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.ideaDetails ? (
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                      </div>
                    ) : (
                      <>
                        <h3 className="font-bold text-sm sm:text-[15px] font-script">Idea title:</h3>
                        <p className="mb-4 font-script text-sm">
                          {accordionData.ideaDetails?.title}
                        </p>
                        <h3 className="font-bold text-sm sm:text-[15px] font-script">Idea description:</h3>
                        <p className="font-script text-sm">{accordionData.ideaDetails?.description}</p>
                      </>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-1">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-purple-400" />
                      <span className="text-sm sm:text-[15px] font-script"> Selected questions for video introduction</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.selectedQuestions ? (
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                      </div>
                    ) : (
                      <ul className="list-disc pl-5 text-sm sm:text-[15px] font-script">
                        {accordionData.selectedQuestions?.map(
                          (question, index) => (
                            <li key={index} className="mb-2">
                              {question}
                            </li>
                          )
                        )}
                      </ul>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <YouTubeIcon className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-red-500" />
                      <span className="text-sm sm:text-[15px] font-script"> YouTube videos that were used</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.youtubeVideos ? (
                      <div className="space-y-4">
                        <Skeleton className="h-24 sm:h-28 w-full" />
                        <Skeleton className="h-24 sm:h-28 w-full" />
                        <Skeleton className="h-24 sm:h-28 w-full" />
                      </div>
                    ) : accordionData.youtubeVideos?.available ? (
                      <div className="space-y-4 sm:space-y-6 text-sm sm:text-[15px] font-script">
                        {accordionData.youtubeVideos.data?.map((video) => (
                          <div
                            key={video.id}
                            className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4"
                          >
                            <a
                              href={`https://www.youtube.com/watch?v=${video.id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex-shrink-0 "
                            >
                              <Image
                                src={`https://img.youtube.com/vi/${video.id}/maxresdefault.jpg`}
                                alt={video.title}
                                width={192}
                                height={112}
                                className="object-cover rounded-md w-full sm:w-48"
                              />
                            </a>
                            <div className="flex flex-col flex-grow">
                              <a
                                href={`https://www.youtube.com/watch?v=${video.id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="font-semibold line-clamp-2 hover:underline"
                              >
                                {video.title}
                              </a>
                              <div className="text-xs sm:text-sm text-gray-400 mt-1 ">
                                <span >{video.views}</span> •{" "}
                                <span>{video.duration}</span> •{" "}
                                <span>{video.publishedTime}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-400">
                        {accordionData.youtubeVideos?.message}
                      </p>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <Globe className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-blue-400" />
                      <span className="text-sm sm:text-[15px] font-script">Webpages that were used</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.webpages ? (
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                      </div>
                    ) : accordionData.webpages?.available ? (
                      <ul className="list-disc pl-5 text-sm sm:text-[15px] font-script">
                        {accordionData.webpages.data?.map((webpage, index) => (
                          <li key={index} className="mb-2">
                            <a
                              href={webpage.url}
                              className="text-blue-400 hover:underline"
                            >
                              {webpage.title}
                            </a>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-400">
                        {accordionData.webpages?.message}
                      </p>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-4">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <FileText className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-green-400" />
                      <span className="text-sm sm:text-[15px] font-script">Research Papers that were used</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.researchPapers ? (
                      <div className="space-y-4">
                        <Skeleton className="h-10 sm:h-12 w-full" />
                        <Skeleton className="h-10 sm:h-12 w-full" />
                        <Skeleton className="h-10 sm:h-12 w-full" />
                      </div>
                    ) : accordionData.researchPapers?.available ? (
                      <ul className="list-disc pl-5 text-sm sm:text-[15px] font-script">
                        {accordionData.researchPapers.data?.map(
                          (paper, index) => (
                            <li key={index} className="mb-4">
                              <a
                                href={paper.url}
                                className="text-blue-400  hover:underline"
                              >
                                <p className="font-semibold">{paper.title}</p>
                              </a>
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p className="text-gray-400">
                        {accordionData.researchPapers?.message}
                      </p>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-5">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <Pencil className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-amber-400" />
                      <span className="text-sm sm:text-[15px] font-script">Custom Data that was used</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-sm sm:text-base">
                    {loading.customData ? (
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4  w-full" />
                        <Skeleton className="h-4 w-full" />
                      </div>
                    ) : accordionData.customData?.available ? (
                      <div className="h-32 sm:h-40 overflow-y-auto pr-2 sm:pr-4 text-sm sm:text-[15px] font-script">
                        <p>{accordionData.customData.data}</p>
                      </div>
                    ) : (
                      <p className="text-gray-400 text-sm sm:text-[15px] font-script">
                        {accordionData.customData?.message}
                      </p>
                    )}
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </div>
        </div>
        <div className="rounded-2xl w-full lg:w-1/2 bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg overflow-hidden">
          <div className="w-full h-full bg-black rounded-2xl py-4 px-2 sm:px-4 overflow-hidden p-4 sm:p-6">
            <div className=" my-2 flex rounded-full w-fit h-fit mx-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
              <div className="bg-black h-full py-2 px-4 rounded-full font-script text-xl font-medium">
                <span className="mr-2">
                  Thought Process
                </span>
                <Switch
                  checked={viewMode === "script"}
                  onCheckedChange={(checked: any) =>
                    setViewMode(checked ? "script" : "thought")
                  }
                />
                <span className="ml-2">Final Script</span>
              </div>
            </div>
            <div className="overflow-y-auto flex-grow px-2 sm:px-4 pt-4">
              {viewMode === "thought" ? (
                <Accordion type="multiple" className="w-full font-script" defaultValue={["item-1", "item-2", "item-3", "item-4", "item-5"]}>
                  <AccordionItem value="item-1">
                    <AccordionTrigger>YouTube Summary</AccordionTrigger>
                    <AccordionContent>
                      {renderAccordionContent(
                        thoughtProcess
                          .filter((paragraph) => paragraph.paragraph.includes("yt "))
                          .map((paragraph, index) => {
                            const updatedParagraph = (() => {
                              const firstOccurrenceIndex = paragraph.paragraph.indexOf("yt");
                              if (firstOccurrenceIndex !== -1) {
                                return paragraph.paragraph.slice(firstOccurrenceIndex + "yt".length);
                              }
                            })();

                            return (
                              <p
                                key={index}
                                className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                              >
                                {updatedParagraph}
                              </p>
                            );
                          }),
                        "youtube-summary"
                      )}
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-2">
                    <AccordionTrigger> Webpage Summary </AccordionTrigger>
                    <AccordionContent>
                      {renderAccordionContent(
                        thoughtProcess
                          .filter((paragraph) => paragraph.paragraph.includes("wp "))
                          .map((paragraph, index) => {
                            const updatedParagraph = (() => {
                              const firstOccurrenceIndex = paragraph.paragraph.indexOf("wp");
                              if (firstOccurrenceIndex !== -1) {
                                return paragraph.paragraph.slice(firstOccurrenceIndex + "wp".length);
                              }
                            })();

                            return (
                              <p
                                key={index}
                                className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                              >
                                {updatedParagraph}
                              </p>
                            );
                          }),
                        "webpage-summary"
                      )}
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-3">
                    <AccordionTrigger>Research Paper Summary</AccordionTrigger>
                    <AccordionContent>
                      {renderAccordionContent(
                        thoughtProcess
                          .filter((paragraph) => paragraph.paragraph.includes("rp "))
                          .map((paragraph, index) => {
                            const updatedParagraph = (() => {
                              const firstOccurrenceIndex = paragraph.paragraph.indexOf("rp");
                              if (firstOccurrenceIndex !== -1) {
                                return paragraph.paragraph.slice(firstOccurrenceIndex + "rp".length);
                              }
                            })();

                            return (
                              <p
                                key={index}
                                className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                              >
                                {updatedParagraph}
                              </p>
                            );
                          }),
                        "research-paper-summary"
                      )}
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-4">
                    <AccordionTrigger>Custom Data Summary</AccordionTrigger>
                    <AccordionContent>
                      {renderAccordionContent(
                        thoughtProcess
                          .filter((paragraph) => paragraph.paragraph.includes("cd "))
                          .map((paragraph, index) => {
                            const updatedParagraph = (() => {
                              const firstOccurrenceIndex = paragraph.paragraph.indexOf("cd");
                              if (firstOccurrenceIndex !== -1) {
                                return paragraph.paragraph.slice(firstOccurrenceIndex + "cd".length);
                              }
                            })();

                            return (
                              <p
                                key={index}
                                className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                              >
                                {updatedParagraph}
                              </p>
                            );
                          }),
                        "custom-data-summary"
                      )}
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-5">
                    <AccordionTrigger>Master Summary</AccordionTrigger>
                    <AccordionContent>
                      {renderAccordionContent(
                        thoughtProcess
                          .filter((paragraph) => paragraph.paragraph.includes("Master Summary"))
                          .map((paragraph, index) => {
                            const updatedParagraph = (() => {
                              const firstOccurrenceIndex = paragraph.paragraph.indexOf("ms");
                              if (firstOccurrenceIndex !== -1) {
                                return paragraph.paragraph.slice(firstOccurrenceIndex + "ms".length);
                              }
                            })();

                            return (
                              <p
                                key={index}
                                className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                              >
                                {updatedParagraph}
                              </p>
                            );
                          }),
                        "master-summary"
                      )}
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              ) : loading.thoughtProcess ? (
                <div className="space-y-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                </div>
              ) : (
                <div className="space-y-4">
                    {/* <p className={`text-sm sm:text-[15px] font-script ${getVisibleColorClass("text-green-500")}`}>
                      {finalScript}
                    </p> */}
                    {thoughtProcess
                      .filter((paragraph) => paragraph.paragraph.includes("Final Script"))
                      .map((paragraph, index) => {
                        const updatedParagraph = (() => {
                          const firstOccurrenceIndex = paragraph.paragraph.indexOf("fs");
                          if (firstOccurrenceIndex !== -1) {
                            return paragraph.paragraph.slice(firstOccurrenceIndex + "fs".length);
                          }
                        })();
                        return (
                          <p
                            key={index}
                            className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(paragraph.color)}`}
                          >
                            {updatedParagraph}
                          </p>
                        );
                      })
                    }
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

