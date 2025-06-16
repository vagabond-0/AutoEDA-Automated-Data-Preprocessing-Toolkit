import { FaUpload, FaCog, FaChartBar, FaDownload } from "react-icons/fa";

const steps = [
  {
    icon: <FaUpload className="h-10 w-10 text-blue-500" />,
    title: "Upload Your Data",
    desc: "Easily upload your dataset or document in one click.",
  },
  {
    icon: <FaCog className="h-10 w-10 text-green-500" />,
    title: "Automated Analysis",
    desc: "Our model processes and analyzes your input automatically.",
  },
  {
    icon: <FaChartBar className="h-10 w-10 text-purple-500" />,
    title: "View Insights",
    desc: "Get instant insights, visualizations, or predictions.",
  },
  {
    icon: <FaDownload className="h-10 w-10 text-yellow-500" />,
    title: "Download Results",
    desc: "Export your results for further use.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-white py-16">
      <div className="max-w-5xl mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {steps.map((step, idx) => (
            <div key={idx} className="flex flex-col items-center text-center">
              {step.icon}
              <h3 className="mt-4 text-xl font-semibold">{step.title}</h3>
              <p className="mt-2 text-gray-600">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}