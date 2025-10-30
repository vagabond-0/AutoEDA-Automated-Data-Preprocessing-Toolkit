import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from './ui/input';
import { Button } from './ui/button';
import { UploadCloud } from 'lucide-react';
import ScrollableCard from './scrollCard';
import axios from 'axios';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const showSummary = () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    axios
      .post("http://127.0.0.1:5000/upload_csv", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully:", response.data);
        setSummary(response.data); // set the returned summary json
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading file: " + (error.response?.data?.error || error.message));
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }
    console.log("Uploading file:", selectedFile.name);
    showSummary();
  };

  const handleCancel = () => {
    setSelectedFile(null);
    setSummary(null);
  };

  return (
    <div className="w-full px-4 md:px-16 py-8 flex justify-center items-center">
      <Card className="bg-card text-foreground shadow-lg border border-border rounded-xl w-full max-w-3xl hover:shadow-xl transition-shadow">
        <CardHeader className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900">
              <UploadCloud className="w-6 h-6 text-blue-600 dark:text-blue-300" />
            </div>
            <div>
              <CardTitle className="text-2xl font-semibold">
                Upload Your CSV File
              </CardTitle>
              <CardDescription>
                Select a CSV file to upload for automatic preprocessing
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="relative">
              <Input
                type="file"
                accept=".csv"
                className="file-input absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="file-input"
                onChange={handleFileChange}
              />
              <label
                htmlFor="file-input"
                className="flex flex-col items-center justify-center border-2 border-dashed border-border hover:border-blue-400 bg-background rounded-lg p-8 transition-colors"
              >
                <UploadCloud className="w-10 h-10 text-muted-foreground mb-3" />
                <p className="text-sm font-medium text-muted-foreground mb-1">
                  <span className="text-blue-600 dark:text-blue-400">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-muted-foreground">CSV files only</p>
                {selectedFile && (
                  <p className="text-sm text-muted-foreground mt-2">
                    Selected: {selectedFile.name}
                  </p>
                )}
              </label>
            </div>

            <div className="flex flex-col md:flex-row items-center gap-3">
              <Button
                type="submit"
                variant="default"
                className="w-full md:w-auto px-6 py-3"
              >
                Upload File
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                className="w-full md:w-auto px-6 py-3"
              >
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>

        {summary && 
          <div className="w-full h-60 border border-[#ccc] rounded-lg shadow-md overflow-y-auto p-4 bg-card dark:text-blue-200 text-blue-950">
            <ScrollableCard data={summary || { message: "No summary available yet." }} />
          </div>
        }

      </Card>
    </div>
  );
};

export default FileUpload;
