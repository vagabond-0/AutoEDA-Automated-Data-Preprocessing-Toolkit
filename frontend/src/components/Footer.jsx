// import React, { useState, useEffect } from 'react';
// import { Mail, ArrowUp, ExternalLink } from 'lucide-react';
// import { SiGithub } from 'react-icons/si';

// const Footer = () => {
//     const [showScrollTop, setShowScrollTop] = useState(false);

//     const quickLinks = [
//         'About Us', 'How it works', 'Try Our Model', 'Leave a Review', 'Login / Signup'
//     ];

//     useEffect(() => {
//         const handleScroll = () => {
//             setShowScrollTop(window.scrollY > 500);
//         };

//         window.addEventListener('scroll', handleScroll);
//         return () => window.removeEventListener('scroll', handleScroll);
//     }, []);

//     const scrollToTop = () => {
//         window.scrollTo({ top: 0, behavior: 'smooth' });
//     };

//     return (
//         <footer className="relative bg-slate-900 border-t border-slate-700/50 overflow-hidden">
//             {/* Background Effects */}
//             <div className="absolute inset-0">
//                 <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl"></div>
//                 <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-blue-500/5 rounded-full blur-3xl"></div>
//                 <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-900/95 to-slate-800/90"></div>
//             </div>

//             <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
//                 {/* Main Footer Content */}
//                 <div className="py-16">
//                     <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
//                         {/* Brand Section */}
//                         <div className="lg:col-span-6">
//                             {/* Logo and Brand */}
//                             <div className="flex items-center space-x-4 mb-8">
//                                 <div className="relative">
//                                     {/* Logo container */}
//                                     <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/25 overflow-hidden">
//                                         <span className="text-white text-2xl font-bold">A</span>
//                                     </div>
//                                 </div>

//                                 {/* Text content */}
//                                 <div>
//                                     <h3 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-blue-500 bg-clip-text text-transparent mb-1">
//                                         AutoEDA
//                                     </h3>
//                                     <p className="text-slate-400 font-medium tracking-wide">Automated Exploratory Data Analysis</p>
//                                 </div>
//                             </div>

//                             {/* Description */}
//                             <p className="text-slate-300 text-lg leading-relaxed mb-8 max-w-lg">
//                                 <span className="font-semibold text-blue-400">Instant insights, zero hassle.</span>
//                                 <br />
//                                 Empower your data journey with our automated analysis platform.
//                             </p>
//                         </div>

//                         {/* Links Section */}
//                         <div className="lg:col-span-6">
//                             <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
//                                 {/* Quick Links */}
//                                 <div>
//                                     <h4 className="text-xl font-bold text-white mb-6 relative">
//                                         Quick Links
//                                         <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                                     </h4>
//                                     <ul className="space-y-3">
//                                         {quickLinks.map((link, index) => (
//                                             <li key={index}>
//                                                 <a
//                                                     href="#"
//                                                     className="text-slate-400 hover:text-blue-400 transition-all duration-300 font-medium flex items-center space-x-3 group py-1"
//                                                 >
//                                                     <div className="w-1.5 h-1.5 bg-slate-600 rounded-full group-hover:bg-blue-400 transition-colors duration-300"></div>
//                                                     <span>{link}</span>
//                                                     <ExternalLink className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-0 group-hover:translate-x-1" />
//                                                 </a>
//                                             </li>
//                                         ))}
//                                     </ul>
//                                 </div>

//                                 {/* Contact Info */}
//                                 <div>
//                                     <h4 className="text-xl font-bold text-white mb-6 relative">
//                                         Contact
//                                         <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                                     </h4>
//                                     <div className="space-y-4">
//                                         <div className="flex items-center space-x-4 text-slate-300 hover:text-blue-400 transition-colors duration-300 group cursor-pointer">
//                                             <div className="w-10 h-10 bg-slate-800/50 rounded-lg flex items-center justify-center group-hover:bg-blue-500/10 transition-colors duration-300">
//                                                 <Mail className="w-5 h-5 text-blue-400" />
//                                             </div>
//                                             <span className="font-medium">contact@autoeda.com</span>
//                                         </div>
//                                         <div className="flex items-center space-x-4 text-slate-300 hover:text-blue-400 transition-colors duration-300 group cursor-pointer">
//                                             <div className="w-10 h-10 bg-slate-800/50 rounded-lg flex items-center justify-center group-hover:bg-blue-500/10 transition-colors duration-300">
//                                                 <SiGithub className="w-5 h-5 text-blue-400" />
//                                             </div>
//                                             <a href="https://github.com/AutoEDA" className="font-medium">GitHub Repository</a>
//                                         </div>
//                                     </div>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </div>

//                 {/* Bottom Footer */}
//                 <div className="py-6 border-t border-slate-800/50">
//                     <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
//                         <div className="text-slate-400">
//                             © 2025 AutoEDA. All rights reserved.
//                         </div>

//                         <div className="flex items-center space-x-8">
//                             <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                 Privacy Policy
//                             </a>
//                             <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                 Terms of Service
//                             </a>
//                         </div>
//                     </div>
//                 </div>
//             </div>

//             {/* Scroll to Top Button */}
//             {showScrollTop && (
//                 <button
//                     onClick={scrollToTop}
//                     className="fixed bottom-8 right-8 p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-2xl shadow-2xl shadow-blue-500/25 hover:shadow-blue-500/50 hover:scale-110 transition-all duration-300 z-50 group"
//                 >
//                     <ArrowUp className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
//                 </button>
//             )}
//         </footer>
//     );
// };

// export default Footer;



//---------------------------------------------------------------------------------------------

















// import React, { useState, useEffect } from 'react';
// import { Mail, ArrowUp, ExternalLink } from 'lucide-react';
// import { SiGithub } from 'react-icons/si';

// const Footer = () => {
//     const [showScrollTop, setShowScrollTop] = useState(false);

//     useEffect(() => {
//         const handleScroll = () => {
//             setShowScrollTop(window.scrollY > 500);
//         };

//         window.addEventListener('scroll', handleScroll);
//         return () => window.removeEventListener('scroll', handleScroll);
//     }, []);

//     const scrollToTop = () => {
//         window.scrollTo({ top: 0, behavior: 'smooth' });
//     };

//     return (
//         <footer className="relative bg-slate-900 border-t border-slate-700/50 overflow-hidden">
//             {/* Background Effects */}
//             <div className="absolute inset-0">
//                 <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl"></div>
//                 <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-blue-500/5 rounded-full blur-3xl"></div>
//                 <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-900/95 to-slate-800/90"></div>
//             </div>

//             <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
//                 {/* Main Footer Content */}
//                 <div className="py-16">
//                     <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
//                         {/* Company Section */}
//                         <div>
//                             <h4 className="text-lg font-bold text-white mb-6 relative">
//                                 Company
//                                 <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                             </h4>
//                             <ul className="space-y-3">
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         About Us
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Our Team
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Research
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Events
//                                     </a>
//                                 </li>
//                             </ul>
//                         </div>

//                         {/* Support Section */}
//                         <div>
//                             <h4 className="text-lg font-bold text-white mb-6 relative">
//                                 Support
//                                 <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                             </h4>
//                             <ul className="space-y-3">
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Contact Us
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         FAQ
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Community
//                                     </a>
//                                 </li>
//                             </ul>
//                         </div>

//                         {/* Legal Section */}
//                         <div>
//                             <h4 className="text-lg font-bold text-white mb-6 relative">
//                                 Legal
//                                 <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                             </h4>
//                             <ul className="space-y-3">
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Privacy Policy
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Terms of Service
//                                     </a>
//                                 </li>
//                                 <li>
//                                     <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                         Cookie Policy
//                                     </a>
//                                 </li>
//                             </ul>
//                         </div>

//                         {/* Contact Section */}
//                         <div>
//                             <h4 className="text-lg font-bold text-white mb-6 relative">
//                                 Contact
//                                 <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full"></div>
//                             </h4>
//                             <div className="space-y-4">
//                                 <div className="flex items-start space-x-4 text-slate-300 hover:text-blue-400 transition-colors duration-300">
//                                     <Mail className="w-5 h-5 text-blue-400 mt-1 flex-shrink-0" />
//                                     <a href="mailto:contact@autoeda.com" className="font-medium hover:underline">
//                                         contact@autoeda.com
//                                     </a>
//                                 </div>
//                                 <div className="flex items-start space-x-4 text-slate-300 hover:text-blue-400 transition-colors duration-300">
//                                     <SiGithub className="w-5 h-5 text-blue-400 mt-1 flex-shrink-0" />
//                                     <a href="https://github.com/AutoEDA" className="font-medium hover:underline">
//                                         GitHub Repository
//                                     </a>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </div>

//                 {/* Bottom Footer */}
//                 <div className="py-6 border-t border-slate-800/50">
//                     <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
//                         <div className="text-slate-400 order-2 md:order-1">
//                             © 2025 AutoEDA. All rights reserved.
//                         </div>

//                         <div className="flex items-center space-x-8 order-1 md:order-2">
//                             <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                 Privacy Policy
//                             </a>
//                             <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                 Terms of Service
//                             </a>
//                             <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors duration-300 font-medium">
//                                 Cookie Policy
//                             </a>
//                         </div>
//                     </div>
//                 </div>
//             </div>

//             {/* Scroll to Top Button */}
//             {showScrollTop && (
//                 <button
//                     onClick={scrollToTop}
//                     className="fixed bottom-8 right-8 p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-2xl shadow-2xl shadow-blue-500/25 hover:shadow-blue-500/50 hover:scale-110 transition-all duration-300 z-50 group"
//                 >
//                     <ArrowUp className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
//                 </button>
//             )}
//         </footer>
//     );
// };

// export default Footer;

import React, { useState, useEffect } from 'react';
import { Mail, ArrowUp, ExternalLink } from 'lucide-react';
import { SiGithub } from 'react-icons/si';
import { Linkedin } from 'lucide-react'; 

const Footer = () => {
    const [showScrollTop, setShowScrollTop] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setShowScrollTop(window.scrollY > 500);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <footer className="relative bg-gradient-to-br from-blue-900 via-purple-900 to-slate-900 border-t border-slate-700 overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl"></div>
                <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-purple-600/10 rounded-full blur-3xl"></div>
                <div className="absolute inset-0 bg-gradient-to-br from-blue-900/90 via-purple-900/90 to-slate-900/90"></div>
            </div>

            <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
                {/* Main Footer Content */}
                <div className="py-16">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                        {/* Brand Section - Takes 5 columns */}
                        <div className="lg:col-span-5">
                            {/* Logo and Brand */}
                            <div className="flex items-center space-x-4 mb-8">
                                <div className="relative">
                                    {/* Logo container */}
                                    <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-purple-500/25 overflow-hidden">
                                        <span className="text-white text-2xl font-bold">A</span>
                                    </div>
                                </div>

                                {/* Text content */}
                                <div>
                                    <h3 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-1">
                                        AutoEDA
                                    </h3>
                                    <p className="text-slate-300 font-medium tracking-wide">Automated Exploratory Data Analysis</p>
                                </div>
                            </div>

                            {/* Description */}
                            <p className="text-slate-300 text-lg leading-relaxed mb-8 max-w-lg">
                                <span className="font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Instant insights, zero hassle.</span>
                                <br />
                                Empower your data journey with our automated analysis platform.
                            </p>
                        </div>

                        {/* Links Section - Takes 7 columns (divided into 4 parts) */}
                        <div className="lg:col-span-7">
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                                {/* Company Section */}
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-6 relative">
                                        Company
                                        <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                                    </h4>
                                    <ul className="space-y-3">
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                About Us
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Our Team
                                            </a>
                                        </li>
                                       
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Events
                                            </a>
                                        </li>
                                    </ul>
                                </div>

                                {/* Support Section */}
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-6 relative">
                                        Support
                                        <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                                    </h4>
                                    <ul className="space-y-3">
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Contact Us
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                FAQ
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Community
                                            </a>
                                        </li>
                                    </ul>
                                </div>

                                {/* Legal Section */}
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-6 relative">
                                        Legal
                                        <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                                    </h4>
                                    <ul className="space-y-3">
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Privacy Policy
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Terms of Service
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                                Cookie Policy
                                            </a>
                                        </li>
                                    </ul>
                                </div>

                                {/* Contact Section */}
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-6 relative">
                                        Contact
                                        <div className="absolute -bottom-2 left-0 w-12 h-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                                    </h4>
                                    <div className="space-y-4">
                                     
                                        <div className="flex items-start space-x-4 text-slate-300 hover:text-blue-300 transition-colors duration-300">
                                            <Mail className="w-5 h-5 text-blue-300 mt-1 flex-shrink-0" />
                                            <a href="mailto:satyapriyanidhi@gmail.com" className="font-medium hover:underline">
                                                Email
                                            </a>
                                        </div>
                                        <div className="flex items-start space-x-4 text-slate-300 hover:text-blue-300 transition-colors duration-300">
                                            <SiGithub className="w-5 h-5 text-blue-300 mt-1 flex-shrink-0" />
                                            <a href="https://github.com/Nidhi-Satyapriya/AutoEDA-Automated-Data-Preprocessing-Toolkit" className="font-medium hover:underline">
                                                GitHub 
                                            </a>
                                        </div>
                                        {/* LinkedIn */}
                                        <div className="flex items-start space-x-4 text-slate-300 hover:text-blue-300 transition-colors duration-300">
                                            <Linkedin className="w-5 h-5 text-blue-300 mt-1 flex-shrink-0" />
                                            <a href="https://www.linkedin.com/in/nidhi-satyapriya-960556249/" className="font-medium hover:underline">
                                                LinkedIn
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Footer */}
                <div className="py-6 border-t border-slate-700/50">
                    <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
                        <div className="text-slate-400 order-2 md:order-1">
                            © 2025 AutoEDA. All rights reserved.
                        </div>

                        <div className="flex items-center space-x-8 order-1 md:order-2">
                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                Privacy Policy
                            </a>
                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                Terms of Service
                            </a>
                            <a href="#" className="text-slate-300 hover:text-blue-300 transition-colors duration-300 font-medium">
                                Cookie Policy
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Scroll to Top Button */}
            {showScrollTop && (
                <button
                    onClick={scrollToTop}
                    className="fixed bottom-8 right-8 p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl shadow-2xl shadow-purple-500/25 hover:shadow-purple-500/50 hover:scale-110 transition-all duration-300 z-50 group"
                >
                    <ArrowUp className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
                </button>
            )}
        </footer>
    );
};

export default Footer;