"use client";

import { useState, useEffect } from "react";
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
import {
  // Edit,
  Lightbulb,
  MessageSquare,
  Globe,
  FileText,
  Pencil,
} from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import Image from "next/image";

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
  const [thoughtProcess, setThoughtProcess] = useState<
    ThoughtProcessParagraph[]
  >([]);
  const [finalScript, setFinalScript] = useState<string>("");


  // -----------------------------------------------------------------
  const [displayedText, setDisplayedText] = useState("");
  const [isScriptAnimationComplete, setIsScriptAnimationComplete] = useState(false);

  useEffect(() => {
    if (finalScript && !isScriptAnimationComplete) {
      let currentIndex = 0;
      
      const animateText = () => {
        if (currentIndex < finalScript.length) {
          setDisplayedText(prev => prev + finalScript[currentIndex]);
          currentIndex++;
          scriptAnimationTimeout = setTimeout(animateText, 30);
        } else {
          setIsScriptAnimationComplete(true);
        }
      };

      let scriptAnimationTimeout = setTimeout(animateText, 30);
      
      return () => {
        if (scriptAnimationTimeout) {
          clearTimeout(scriptAnimationTimeout);
        }
      };
    }
  }, [finalScript]);

  // ---------------------------------------------------------------------

    const [displayedThoughts, setDisplayedThoughts] = useState<ThoughtProcessParagraph[]>([]);
    const [isThoughtAnimationComplete, setIsThoughtAnimationComplete] = useState(false);
  
    useEffect(() => {
    // Thought process animation
    if (thoughtProcess.length > 0 && !isThoughtAnimationComplete) {
      let currentIndex = 0;
      let currentCharIndex = 0;
      let currentThought = thoughtProcess[0];
      let tempThoughts: ThoughtProcessParagraph[] = [];
      
      const animateThoughts = () => {
        if (currentIndex >= thoughtProcess.length) {
          setIsThoughtAnimationComplete(true);
          return;
        }

        if (currentCharIndex === 0) {
          tempThoughts = [...tempThoughts, { paragraph: "", color: currentThought.color }];
        }

        if (currentCharIndex < currentThought.paragraph.length) {
          tempThoughts[currentIndex] = {
            paragraph: currentThought.paragraph.slice(0, currentCharIndex + 1),
            color: currentThought.color
          };
          setDisplayedThoughts([...tempThoughts]);
          currentCharIndex++;
          thoughtAnimationTimeout = setTimeout(animateThoughts, 30);
        } else {
          currentIndex++;
          if (currentIndex < thoughtProcess.length) {
            currentThought = thoughtProcess[currentIndex];
            currentCharIndex = 0;
            thoughtAnimationTimeout = setTimeout(animateThoughts, 30);
          } else {
            setIsThoughtAnimationComplete(true);
          }
        }
      };

      let thoughtAnimationTimeout = setTimeout(animateThoughts, 30);
      
      return () => {
        if (thoughtAnimationTimeout) {
          clearTimeout(thoughtAnimationTimeout);
        }
      };
    }
  }, [thoughtProcess]);

  //-----------------------------------------------------------------------------

  useEffect(() => {
    if (loading.thoughtProcess || loading.finalScript) {
      setDisplayedThoughts([]);
      setDisplayedText("");
      setIsThoughtAnimationComplete(false);
      setIsScriptAnimationComplete(false);
    }
  }, [loading.thoughtProcess, loading.finalScript]);

  //-----------------------------------------------------------------------------

  useEffect(() => {
    if (!isLoaded || !isSignedIn || !projectID) {
      return
    }
    const payload = {
      userEmail: user?.primaryEmailAddress?.emailAddress,
      projectID: projectID
    }
    const fetchData = async (endpoint: string, key: keyof typeof loading) => {
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
            setFinalScript(data);
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

    fetchData("getVideoTitle", "projectTitle");
    fetchData("getIdeaDetails", "ideaDetails");
    fetchData("getSelectedQuestions", "selectedQuestions");
    fetchData("getYoutubeVideos", "youtubeVideos");
    fetchData("getWebPages", "webpages");
    fetchData("getResearchPapers", "researchPapers");
    fetchData("getCustomData", "customData");
    fetchData("getThoughtProcess", "thoughtProcess");
    fetchData("getFinalScript", "finalScript");
  }, [isLoaded, isSignedIn, user, projectID]);

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
        <h1 className="text-2xl sm:text-3xl font-bold mb-4 sm:mb-8 text-center">
          {projectTitle}
        </h1>
      )}

      <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 flex-grow h-full lg:h-full overflow-hidden">
        <div className=" flex rounded-2xl w-full lg:w-1/2 bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg overflow-hidden">
          <div className="w-full h-full bg-black rounded-2xl py-4 px-2 sm:px-4 overflow-hidden p-4 sm:p-6">
            {/* <div className="w-full lg:w-1/2 bg-gray-900 rounded-lg p-4 sm:p-6 flex flex-col overflow-hidden"> */}
            <h2 className="text-2xl sm:text-4xl font-semibold mb-4 sm:mb-6 text-center">
              Details
            </h2>
            <div className="overflow-y-auto flex-grow w-full pr-2 sm:pr-4">
              <Accordion type="multiple" className="w-full">
                <AccordionItem value="item-0">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <Lightbulb className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-yellow-400" />
                      <span>Idea Details</span>
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
                        <h3 className="font-bold text-lg">Idea title:</h3>
                        <p className="mb-4">
                          {accordionData.ideaDetails?.title}
                        </p>
                        <h3 className="font-bold text-lg">Idea description:</h3>
                        <p>{accordionData.ideaDetails?.description}</p>
                      </>
                    )}
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-1">
                  <AccordionTrigger className="text-lg sm:text-xl justify-between hover:no-underline">
                    <div className="flex items-center">
                      <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5 mr-2 flex-shrink-0 text-purple-400" />
                      <span>Selected questions for video introduction</span>
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
                      <ul className="list-disc pl-5">
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
                      <span>YouTube videos that were used</span>
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
                      <div className="space-y-4 sm:space-y-6">
                        {accordionData.youtubeVideos.data?.map((video) => (
                          <div
                            key={video.id}
                            className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4"
                          >
                            <a
                              href={`https://www.youtube.com/watch?v=${video.id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex-shrink-0"
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
                              <div className="text-xs sm:text-sm text-gray-400 mt-1">
                                <span>{video.views}</span> •{" "}
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
                      <span>Webpages that were used</span>
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
                      <ul className="list-disc pl-5">
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
                      <span>Research Papers that were used</span>
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
                      <ul className="list-disc pl-5">
                        {accordionData.researchPapers.data?.map(
                          (paper, index) => (
                            <li key={index} className="mb-4">
                              <a
                                href={paper.url}
                                className="text-blue-400  hover:underline"
                              >
                                <p className="font-semibold">{paper.title}</p>
                                {/* <p className="text-xs sm:text-sm">
                                  by {paper.authors}
                                </p> */}
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
                      <span>Custom Data that was used</span>
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
                      <div className="h-32 sm:h-40 overflow-y-auto pr-2 sm:pr-4">
                        <p>{accordionData.customData.data}</p>
                      </div>
                    ) : (
                      <p className="text-gray-400">
                        {accordionData.customData?.message}
                      </p>
                    )}
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>

            {/* <div className="mt-6 mx-auto relative group flex w-full sm:w-[80%] md:w-[70%] lg:w-[600px] justify-center h-fit ">
              <div className="absolute inset-0 blur-xl rounded-full w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative flex rounded-full w-full h-fit bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                <Button
                  className="h-fit text-base sm:text-lg md:text-xl lg:text-2xl text-wrap"
                  variant="gradient"
                > */}
                  {/* <Edit className="mr-2 h-5 w-5" /> */}
                  {/* Update Details and Rerun Project
                </Button>
              </div>
            </div> */}
          </div>
        </div>
        <div className="rounded-2xl w-full lg:w-1/2 bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg overflow-hidden">
          <div className="w-full h-full bg-black rounded-2xl py-4 px-2 sm:px-4 overflow-hidden p-4 sm:p-6">
            {/* <div className="w-full lg:w-1/2 bg-gray-900 rounded-lg p-4 sm:p-6 flex flex-col overflow-hidden"> */}
            {/* <h2 className="text-2xl sm:text-4xl font-semibold mb-4 sm:mb-6 text-center">
              {viewMode === "thought" ? "Thought Process" : "Final Script"}
            </h2> */}
            <div className=" my-2 flex rounded-full w-fit h-fit mx-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
              <div className="bg-black h-full py-2 px-4 rounded-full">
                <span className="mr-2 text-2xl">
                  Thought Process
                </span>
                <Switch
                  checked={viewMode === "script"}
                  onCheckedChange={(checked: any) =>
                    setViewMode(checked ? "script" : "thought")
                  }
                />
                <span className="ml-2 text-2xl">Final Script</span>
              </div>
            </div>
            <div className="overflow-y-auto flex-grow px-2 sm:px-4 pt-4">
              {viewMode === "thought" ? (
                loading.thoughtProcess ? (
                  <div className="space-y-4">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                  </div>
                ) : (
                  // <div className="space-y-4">
                  //   {displayedThoughts.map((paragraph, index) => (
                  //     <p
                  //       key={index}
                  //       className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(
                  //         paragraph.color
                  //       )}`}
                  //     >
                  //       {paragraph.paragraph}
                  //     </p>
                  //   ))}
                  // </div>
                  <div className="space-y-4">
                    {thoughtProcess.map((paragraph, index) => (
                      <p
                        key={index}
                        className={`text-sm sm:text-[15px] font-script py-3 ${getVisibleColorClass(
                          paragraph.color
                        )}`}
                      >
                        {paragraph.paragraph}
                      </p>
                    ))}
                  </div>
                )
              ) : loading.finalScript ? (
                <div className="space-y-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                </div>
              ) : (
                // <p className="text-sm sm:text-lg">{finalScript}</p>
                <div className="space-y-4">
                    <p className={`text-sm sm:text-[15px] font-script ${getVisibleColorClass("text-green-500")}`}>
                      {/* {finalScript} */}
                      {displayedText}
                    </p>
                </div>
              )}
            </div>
            {/* <div className="flex items-center justify-center mt-4 sm:mt-6 mx-auto bg-gray-800 w-fit p-2 rounded-full px-4"> */}
            {/* <div className="mt-6 mx-auto relative group flex w-fit justify-center h-fit p-2 rounded-full px-4"> */}
            
            {/* </div> */}
          </div>
        </div>
        {/* </div> */}
      </div>
    </div>
  );
}
