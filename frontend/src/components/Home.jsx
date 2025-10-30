import React from 'react';
import About from './About';
import HowItWorks from './HowItWorks';
import FileUpload from './FileUpload';
import Navbar from './Navbar';
import Contact from './Contact';

export default function Home() {
  return (
    <div className="relative w-full min-h-screen flex flex-col bg-background text-foreground">
      <Navbar />
      <div className="pt-16">
        <section id="about">
          <About />
        </section>
        <section id="how-it-works">
          <HowItWorks />
        </section>
        <section id="upload">
          <FileUpload />
        </section>
        <section id="contact">
          <Contact />
        </section>
      </div>
    </div>
  );
}
