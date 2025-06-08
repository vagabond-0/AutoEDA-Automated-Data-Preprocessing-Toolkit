import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from 'react-router-dom';

const AuthForm = ({ isLogin, toggleForm }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    try {
      console.log(`${isLogin ? "Logging in" : "Signing up"}`, data);
                           //API CALL TO AUTHENTICATION ENDPOINT
      navigate('/dashboard');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {!isLogin && (
        <div>
          <Input 
            placeholder="Name" 
            {...register("name", { 
              required: "Name is required",
              minLength: {
                value: 2,
                message: "Name must be at least 2 characters"
              }
            })} 
          />
          {errors.name && (
            <p className="text-sm text-red-500 flex items-center gap-1 mt-1">
              {errors.name.message}
            </p>
          )}
        </div>
      )}

      <div>
        <Input 
          placeholder="Email" 
          type="email" 
          {...register("email", { 
            required: "Email is required",
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "Invalid email address"
            }
          })} 
        />
        {errors.email && (
          <p className="text-sm text-red-500 flex items-center gap-1 mt-1">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <Input 
          placeholder="Password" 
          type="password" 
          {...register("password", { 
            required: "Password is required",
            minLength: {
              value: 8,
              message: "Password must be at least 8 characters"
            }
          })} 
        />
        {errors.password && (
          <p className="text-sm text-red-500 flex items-center gap-1 mt-1">
            {errors.password.message}
          </p>
        )}
      </div>

      <Button 
        type="submit" 
        className="w-full"
        disabled={isSubmitting}
      >
        {isSubmitting ? (
          <span className="flex items-center justify-center">
            <motion.span
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="inline-block h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"
            />
            {isLogin ? "Logging in..." : "Signing up..."}
          </span>
        ) : isLogin ? "Login" : "Sign Up"}
      </Button>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300/20" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Or continue with
          </span>
        </div>
      </div>

      <Button variant="outline" className="w-full" type="button">
        Google
      </Button>

      <p className="text-center text-sm text-muted-foreground mt-4">
        {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
        <button
          type="button"
          onClick={toggleForm}
          className="font-medium text-primary hover:underline"
        >
          {isLogin ? "Sign up" : "Log in"}
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
    <div className="min-h-screen flex flex-col-reverse md:flex-row items-stretch">
      <div className="flex-1 flex items-center justify-center p-4 md:p-8 bg-background">
        <AnimatePresence mode="wait">
          <motion.div
            key={isLogin ? "login" : "signup"}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
            className="w-full max-w-md"
          >
            <Card className="border-0 shadow-none md:border md:shadow-sm">
              <CardContent className="p-6 md:p-8">
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <h1 className="text-2xl font-bold text-center mb-1">
                    {isLogin ? "Welcome back" : "Create an account"}
                  </h1>
                  <p className="text-sm text-muted-foreground text-center mb-6">
                    {isLogin ? "Enter your credentials to sign in" : "Enter your details to get started"}
                  </p>
                  <AuthForm isLogin={isLogin} toggleForm={toggleForm} />
                </motion.div>
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
              alt=""
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-black/30 md:bg-gradient-to-r md:from-black/80 md:to-black/30" />
            <div className="absolute bottom-8 left-8 text-white">
              <motion.h2 
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-2xl md:text-4xl font-bold mb-2"
              >
                {!isLogin ? "Discover amazing content" : "Join our community"}
              </motion.h2>
              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="text-sm md:text-base max-w-md"
              >
                {!isLogin ? "Sign in to access your personalized dashboard" : "Create an account to unlock all features"}
              </motion.p>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}