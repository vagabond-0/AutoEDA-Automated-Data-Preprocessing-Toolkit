import { FaUpload, FaCog, FaChartBar, FaDownload } from "react-icons/fa";

const steps = [
  {
    icon: <FaUpload className="h-10 w-10 text-blue-500 dark:text-blue-400" />,
    title: "Upload Your Data",
    desc: "Easily upload your dataset or document in one click.",
  },
  {
    icon: <FaCog className="h-10 w-10 text-green-500 dark:text-green-400" />,
    title: "Automated Analysis",
    desc: "Our model processes and analyzes your input automatically.",
  },
  {
    icon: <FaChartBar className="h-10 w-10 text-purple-500 dark:text-purple-400" />,
    title: "View Insights",
    desc: "Get instant insights, visualizations, or predictions.",
  },
  {
    icon: <FaDownload className="h-10 w-10 text-yellow-500 dark:text-yellow-400" />,
    title: "Download Results",
    desc: "Export your results for further use.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-background py-12">
      <div className="w-full px-4 md:px-16 flex justify-center items-center">
        <div className="bg-card text-foreground shadow-lg border border-border rounded-2xl w-full max-w-5xl px-4 md:px-16 py-12">
          <h2 className="text-3xl font-bold mb-8 text-center">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {steps.map((step, idx) => (
              <div key={idx} className="flex flex-col items-center text-center">
                {step.icon}
                <h3 className="mt-4 text-xl font-semibold">{step.title}</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-300">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}