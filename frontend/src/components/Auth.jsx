import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from 'react-router-dom';
import { Loader2, Eye, EyeOff, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth0 } from "@auth0/auth0-react";


const AuthForm = ({ isLogin, toggleForm }) => {
  const {user, loginWithRedirect, isAuthenticated, logout} = useAuth0();
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setError,
    clearErrors,
  } = useForm();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState(null);
  const navigate = useNavigate();
  const password = watch('password');

  const passwordStrength = () => {
    if (!password) return 0;
    let strength = 0;
    if (password.length >= 8) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    return strength;
  };

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setAuthError(null);
    clearErrors('root');
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const endpoint = isLogin ? '/login' : '/signup';
      
      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
          ...(isLogin ? {} : { name: data.name })
        }),
        credentials: 'include'
      });
      
      const result = await response.json();
      
      if (!response.ok) {
        setAuthError(result.message || 'Authentication failed. Please try again.');
        return;
      }
      if (result.token) {
        localStorage.setItem('authToken', result.token);
      }
      
      if (result.user) {
        localStorage.setItem('user', JSON.stringify(result.user));
      }
      
      toast.success(result.message || (isLogin ? 'Login successful!' : 'Account created successfully!'));
      
      navigate('/');
      
    } catch (error) {
      console.error('Authentication error:', error);
      setAuthError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {authError && (
        <div className="p-3 rounded-md bg-red-50 border border-red-200 flex items-start gap-2">
          <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-red-600">{authError}</p>
        </div>
      )}
      
      {!isLogin && (
        <div className="space-y-1.5">
          <Input 
            placeholder="Full name" 
            {...register("name", { 
              required: "Name is required",
              minLength: {
                value: 2,
                message: "Name must be at least 2 characters"
              }
            })} 
            className="h-11 text-base"
          />
          {errors.name && (
            <p className="text-sm text-red-500 mt-1">
              {errors.name.message}
            </p>
          )}
        </div>
      )}

      <div className="space-y-1.5">
        <Input 
          placeholder="Email address" 
          type="email" 
          {...register("email", { 
            required: "Email is required",
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "Invalid email address"
            }
          })}
          className="h-11 text-base"
        />
        {errors.email && (
          <p className="text-sm text-red-500 mt-1">
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-1.5">
        <div className="relative">
          <Input 
            placeholder="Password" 
            type={showPassword ? "text" : "password"} 
            {...register("password", { 
              required: "Password is required",
              minLength: {
                value: 8,
                message: "Password must be at least 8 characters"
              }
            })}
            className="h-11 text-base pr-10"
          />
          <button
            type="button"
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
        
        {!isLogin && password && (
          <div className="flex gap-1 mt-1">
            {[1, 2, 3, 4].map((i) => (
              <div 
                key={i}
                className={`h-1 flex-1 rounded-sm ${
                  passwordStrength() >= i 
                    ? passwordStrength() >= 3 ? 'bg-green-500' : 'bg-yellow-500'
                    : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        )}

        {errors.password && (
          <p className="text-sm text-red-500 mt-1">
            {errors.password.message}
          </p>
        )}
      </div>

      {isLogin && (
        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center space-x-2">
            <input type="checkbox" className="rounded border-gray-300 text-primary focus:ring-primary" />
            <span>Remember me</span>
          </label>
          <button type="button" className="text-primary hover:underline">
            Forgot password?
          </button>
        </div>
      )}

      <Button 
        type="submit" 
        className="w-full h-11 text-base font-medium"
        disabled={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            {isLogin ? "Logging in..." : "Signing up..."}
          </>
        ) : isLogin ? "Sign in" : "Create account"}
      </Button>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-3 text-gray-500 text-sm">
            Or continue with
          </span>
        </div>
      </div>

     <Button 
       variant="outline" 
       className="w-full py-5 sm:py-6 text-sm sm:text-base flex items-center justify-center gap-2" 
       type="button"
       onClick={() => loginWithRedirect()}
     >
       <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24">
         <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
         <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
         <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" />
         <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
       </svg>
       Google
     </Button>

      <p className="text-center text-sm text-gray-600 mt-4">
        {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
        <button
          type="button"
          onClick={toggleForm}
          className="font-medium text-primary hover:underline"
        >
          {isLogin ? "Sign up" : "Sign in"}
        </button>
      </p>
    </form>
  );
};

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const toggleForm = () => setIsLogin((prev) => !prev);

  const loginImg = "https://images.unsplash.com/photo-1711409254907-fda1c4e05be0?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
  const signupImg = "https://plus.unsplash.com/premium_photo-1682795706814-3e26c44105fd?q=80&w=2012&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

  return (
    <div className="min-h-screen flex flex-col-reverse md:flex-row items-stretch bg-white">
      <div className="flex-1 flex items-center justify-center p-6 md:p-12">
        <AnimatePresence mode="wait">
          <motion.div
            key={isLogin ? "login" : "signup"}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -30 }}
            transition={{ duration: 0.3 }}
            className="w-full max-w-md"
          >
            <Card className="border-0 shadow-none md:border md:shadow-sm rounded-xl">
              <CardContent className="p-8">
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="flex flex-col items-center mb-6"
                >
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <svg 
                      className="w-6 h-6 text-primary" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        strokeWidth="2" 
                        d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"
                      />
                    </svg>
                  </div>
                  <h1 className="text-2xl font-bold text-center">
                    {isLogin ? "Welcome back" : "Create an account"}
                  </h1>
                  <p className="text-sm text-gray-500 text-center mt-2">
                    {isLogin ? "Enter your credentials to sign in" : "Enter your details to get started"}
                  </p>
                </motion.div>
                <AuthForm isLogin={isLogin} toggleForm={toggleForm} />
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>
      </div>

      <div className="relative w-full md:w-1/2 h-64 md:h-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={isLogin ? "loginImg" : "signupImg"}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            className="absolute inset-0"
          >
            <img
              src={isLogin ? loginImg : signupImg}
              alt="Auth background"
              className="w-full h-full object-cover"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-black/30 md:bg-gradient-to-r md:from-black/70 md:to-black/30" />
            <div className="absolute bottom-8 left-8 text-white">
              <motion.h2 
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-2xl md:text-3xl lg:text-4xl font-bold mb-2"
              >
                {isLogin ? "Join our community" : "Discover amazing content"}
              </motion.h2>
              <motion.p
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="text-sm md:text-base max-w-xs md:max-w-md"
              >
                {isLogin ? "Create an account to unlock all features" : "Sign in to access your personalized dashboard"}
              </motion.p>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}