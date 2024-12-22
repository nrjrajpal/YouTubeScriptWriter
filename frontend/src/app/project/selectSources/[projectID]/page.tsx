"use client";

import { useUser } from '@clerk/nextjs'
import { useParams, useRouter } from 'next/navigation'
import { useState, useCallback, useEffect } from "react";
import { Globe, FileText, Pencil, Check } from "lucide-react";
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

  const features = [
    {
      icon: YouTubeIcon,
      title: "YouTube Videos",
      color: "text-red-500",
      buttonText: "Add Custom Links",
      dialogTitle: "Add YouTube Video Links",
      subText:
        "Enter up to 3 YouTube video links. Empty fields will be filled with automatically fetched videos later.",
      points: [
        "Uses transcripts of YouTube videos",
        "Fetches English transcripts for script information",
        "Extracts diverse insights from video content",
      ],
    },
    {
      icon: Globe,
      title: "Web Pages",
      color: "text-blue-400",
      buttonText: "Add Custom Links",
      dialogTitle: "Add Web Page Links",
      subText:
        "Enter up to 3 web page URLs. Empty fields will be filled with automatically fetched web pages later.",
      points: [
        "Crawls web pages to gather detailed content",
        "Prioritizes reliable and relevant web sources",
      ],
    },
    {
      icon: FileText,
      title: "Research Papers",
      color: "text-green-400",
      buttonText: "Add Custom Links",
      dialogTitle: "Add Research Paper Links (Direct PDF Links)",
      subText:
        "Enter up to 3 direct PDF links. Empty fields will be filled with automatically fetched research papers later.",
      points: [
        "Retrieves peer-reviewed research papers",
        "Extracts insights backed by data and evidence",
        "Focuses on high-quality academic sources",
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
        "Ensures flexibility for custom material",
      ],
    },
  ];

  const handleSubmit = useCallback(
    (title: string) => {
      if (title === "Custom") {
        console.log(`Submitted for ${title}:`, customText);
      } else {
        console.log(`Submitted for ${title}:`, inputValues[title]);
      }
      setOpenDialog(null);
    },
    [customText, inputValues]
  );

  const handleInputChange = useCallback(
    (title: string, index: number, value: string) => {
      setInputValues((prev) => ({
        ...prev,
        [title]: prev[title].map((v, i) => (i === index ? value : v)),
      }));
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

    console.log("Main submit button clicked");
    console.log("All input values:", inputValues);
    console.log("Custom text:", customText);
    console.log("Selected features:", selectedFeatures);

    const payload = {

      "YouTube Videos_selected": selectedFeatures.includes("YouTube Videos"),
      "YouTube Videos_links": inputValues["YouTube Videos"].filter(
        (link) => link.trim() !== ""
      ),
      "Web Pages_selected": selectedFeatures.includes("Web Pages"),
      "Web Pages_links": inputValues["Web Pages"].filter(
        (link) => link.trim() !== ""
      ),
      "Research Papers_selected": selectedFeatures.includes("Research Papers"),
      "Research Papers_links": inputValues["Research Papers"].filter(
        (link) => link.trim() !== ""
      ),
      Custom_selected: selectedFeatures.includes("Custom"),
      Custom_text: customText,
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
      toast({
        title: "Success",
        description: data.message,
      });
      router.push(`/project/selectQuestions/${projectID}`)

    } catch (error) {
      console.error("Error submitting data:", error);
      toast({
        title: "Error",
        description:
          "An error occurred while submitting the data. Please try again.",
        variant: "destructive",
      });
    }
  }, [inputValues, customText, selectedFeatures, toast]);

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

  const ToggleButton = ({ title }: { title: string }) => (
    <button
      className={`absolute top-2 right-2 w-6 h-6 flex items-center justify-center rounded-full transition-colors ${
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
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl mb-4 sm:mb-6 text-center">
            Select Information Sources
          </h1>
          <p className="text-center text-gray-400 mb-4">
            Click to select or deselect a source. Sources with content will be
            automatically selected, but you can unselect them.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 sm:gap-6 lg:gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className={`bg-gray-900 rounded-lg px-6 sm:px-6 lg:px-8 pb-6 sm:pb-6 lg:pb-8 pt-4 sm:pt-4 lg:pt-6 flex flex-col relative cursor-pointer ${
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
                    className={`w-8 h-8 sm:w-10 sm:h-10 mr-3 sm:mr-4 ${feature.color}`}
                  />
                  <h2 className="text-xl sm:text-2xl font-semibold text-white">
                    {feature.title}
                  </h2>
                </div>
                <ul className="list-disc list-inside space-y-1 sm:space-y-1 text-gray-300 flex-grow text-sm sm:text-base lg:text-lg">
                  {feature.points.map((point, pointIndex) => (
                    <li key={pointIndex}>{point}</li>
                  ))}
                </ul>
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
                      className="rounded-full bg-gray-950 text-white mt-4 sm:mt-6 text-sm sm:text-base lg:text-lg hover:bg-indigo-950 transition-all border-gray-700 border-2 py-4 sm:py-6"
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
                    className="sm:max-w-[90vw] md:max-w-[750px] bg-gray-950 text-white border border-gray-800 w-11/12 p-4 sm:p-6 lg:p-8 rounded-2xl"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <DialogHeader>
                      <DialogTitle className="text-xl sm:text-2xl lg:text-3xl">
                        {feature.dialogTitle}
                      </DialogTitle>
                    </DialogHeader>
                    <p className="text-sm sm:text-base lg:text-lg text-gray-400 mb-2">
                      {feature.subText}
                    </p>
                    <div className="grid gap-3 sm:gap-4 py-3 sm:py-4">
                      {feature.title === "Custom" ? (
                        <Textarea
                          placeholder="Enter your custom information here"
                          value={customText}
                          onChange={(e) =>
                            handleCustomTextChange(e.target.value)
                          }
                          maxLength={20000}
                          className="h-40 sm:h-60 bg-gray-900 text-white text-base sm:text-lg lg:text-xl p-3 sm:p-4"
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
                            className="bg-gray-900 text-white text-base sm:text-lg lg:text-xl p-3 sm:p-4 h-10 sm:h-12 lg:h-14 w-full"
                          />
                        ))
                      )}
                    </div>
                    <Button
                      onClick={() => handleSubmit(feature.title)}
                      variant="default"
                      className="rounded-full bg-white text-black hover:bg-slate-200 transition-all border-slate-400 hover:border-[3px] w-full text-base sm:text-lg lg:text-xl h-10 sm:h-12  lg:h-14"
                    >
                      Submit
                    </Button>
                  </DialogContent>
                </Dialog>
              </div>
            ))}
          </div>
          <div className="my-4 relative group flex w-full sm:w-[80%] md:w-[70%] lg:w-[600px] justify-center mx-auto">
            <div className="absolute inset-0 blur-xl rounded-full w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[3px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative flex rounded-full w-full h-full  bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[3px]">
              <Button
                onClick={handleMainSubmit}
                variant="gradient"
                className="h-auto py-2 sm:py-3 md:py-4 lg:pb-[18px] text-base sm:text-lg md:text-xl lg:text-2xl"
              >
                Submit
              </Button>
            </div>
          </div>
          {/* <Button
            onClick={() =>
              toast({
                title: "Test Toast",
                description: "This is a test toast message",
              })
            }
            className="mt-4"
          >
            Test Toast
          </Button> */}
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
