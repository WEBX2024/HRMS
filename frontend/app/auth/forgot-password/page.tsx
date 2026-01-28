"use client";

import { useState } from "react";
import Link from "next/link";
import { Mail, ArrowLeft, CheckCircle } from "lucide-react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // TODO: Replace with actual API call
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/forgot-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        },
      );

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
      } else {
        setError(
          data.message || "Failed to send reset email. Please try again.",
        );
      }
    } catch (err) {
      setError("Network error. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-mesh flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Back to Login */}
        <Link
          href="/auth/login"
          className="inline-flex items-center text-neutral-600 hover:text-primary mb-8 transition-colors animate-fade-in"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Login
        </Link>

        {/* Card */}
        <div className="card animate-scale-in">
          {!success ? (
            <>
              {/* Header */}
              <div className="text-center mb-8">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-8 h-8 text-primary" />
                </div>
                <h1 className="text-3xl font-bold text-neutral-800 mb-2">
                  Forgot Password?
                </h1>
                <p className="text-neutral-600">
                  No worries! Enter your email and we'll send you reset
                  instructions.
                </p>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-neutral-700 mb-2"
                  >
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-neutral-400 w-5 h-5" />
                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="input pl-12"
                      placeholder="your.email@company.com"
                      required
                      autoFocus
                    />
                  </div>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm animate-fade-in">
                    {error}
                  </div>
                )}

                {/* Submit Button */}
                <button
                  type="submit"
                  className="btn btn-primary w-full"
                  disabled={loading}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <div
                        className="spinner mr-2"
                        style={{ width: "20px", height: "20px" }}
                      />
                      Sending Reset Link...
                    </span>
                  ) : (
                    "Send Reset Link"
                  )}
                </button>
              </form>

              {/* Additional Links */}
              <div className="mt-6 text-center text-sm text-neutral-600">
                Remember your password?{" "}
                <Link
                  href="/auth/login"
                  className="text-primary font-medium hover:underline"
                >
                  Sign In
                </Link>
              </div>
            </>
          ) : (
            /* Success State */
            <div className="text-center py-8 animate-fade-in">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-neutral-800 mb-2">
                Check Your Email
              </h2>
              <p className="text-neutral-600 mb-6">
                We've sent password reset instructions to{" "}
                <strong>{email}</strong>
              </p>
              <p className="text-sm text-neutral-500 mb-8">
                Didn't receive the email? Check your spam folder or{" "}
                <button
                  onClick={() => setSuccess(false)}
                  className="text-primary font-medium hover:underline"
                >
                  try again
                </button>
              </p>
              <Link href="/auth/login" className="btn btn-primary">
                Back to Login
              </Link>
            </div>
          )}
        </div>

        {/* Help Text */}
        <div className="mt-6 text-center text-sm text-neutral-600 animate-fade-in animation-delay-200">
          <p>
            Need help?{" "}
            <Link href="/support" className="text-primary hover:underline">
              Contact Support
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
