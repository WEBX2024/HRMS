"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Form state
  const [formData, setFormData] = useState({
    // Company Information
    company_name: "",
    company_code: "",
    subdomain: "",
    primary_email: "",
    primary_phone: "",
    website: "",

    // Address
    address_line1: "",
    address_line2: "",
    city: "",
    state: "",
    country: "",
    postal_code: "",

    // Admin Information
    admin_first_name: "",
    admin_last_name: "",
    admin_email: "",
    admin_phone: "",

    // Subscription
    subscription_plan: "PROFESSIONAL",

    // Terms
    accept_terms: false,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleNext = () => {
    setError("");
    if (step === 1) {
      // Validate company info
      if (
        !formData.company_name ||
        !formData.company_code ||
        !formData.primary_email
      ) {
        setError("Please fill in all required company fields");
        return;
      }
    } else if (step === 2) {
      // Validate address
      if (!formData.address_line1 || !formData.city || !formData.country) {
        setError("Please fill in all required address fields");
        return;
      }
    } else if (step === 3) {
      // Validate admin info
      if (
        !formData.admin_first_name ||
        !formData.admin_last_name ||
        !formData.admin_email
      ) {
        setError("Please fill in all required admin fields");
        return;
      }
    }
    setStep(step + 1);
  };

  const handleBack = () => {
    setError("");
    setStep(step - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!formData.accept_terms) {
      setError("Please accept the terms and conditions");
      return;
    }

    setLoading(true);

    try {
      // TODO: Replace with actual API call
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/tenants/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            company_name: formData.company_name,
            company_code: formData.company_code,
            subdomain: formData.subdomain,
            primary_email: formData.primary_email,
            primary_phone: formData.primary_phone,
            website: formData.website,
            address: {
              line1: formData.address_line1,
              line2: formData.address_line2,
              city: formData.city,
              state: formData.state,
              country: formData.country,
              postal_code: formData.postal_code,
            },
            admin: {
              first_name: formData.admin_first_name,
              last_name: formData.admin_last_name,
              email: formData.admin_email,
              phone: formData.admin_phone,
            },
            subscription_plan: formData.subscription_plan,
          }),
        },
      );

      const data = await response.json();

      if (response.ok) {
        // Redirect to verification page
        router.push("/auth/verify-email?email=" + formData.admin_email);
      } else {
        setError(data.message || "Signup failed. Please try again.");
      }
    } catch (err) {
      setError("Network error. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-mesh flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl font-bold text-primary mb-2">
            Create Your HRMS Account
          </h1>
          <p className="text-neutral-600">
            Start managing your workforce in minutes
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center mb-8 animate-fade-in-up animation-delay-100">
          <div className="flex items-center space-x-4">
            {[1, 2, 3, 4].map((s) => (
              <div key={s} className="flex items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                    step >= s
                      ? "bg-primary text-white"
                      : "bg-neutral-200 text-neutral-500"
                  }`}
                >
                  {s}
                </div>
                {s < 4 && (
                  <div
                    className={`w-16 h-1 mx-2 transition-all ${
                      step > s ? "bg-primary" : "bg-neutral-200"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Form Card */}
        <div className="card animate-scale-in animation-delay-200">
          <form onSubmit={handleSubmit}>
            {/* Step 1: Company Information */}
            {step === 1 && (
              <div className="space-y-4">
                <h2 className="text-2xl font-semibold mb-4">
                  Company Information
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Company Name *
                    </label>
                    <input
                      type="text"
                      name="company_name"
                      value={formData.company_name}
                      onChange={handleChange}
                      className="input"
                      placeholder="Acme Corporation"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Company Code *
                    </label>
                    <input
                      type="text"
                      name="company_code"
                      value={formData.company_code}
                      onChange={handleChange}
                      className="input"
                      placeholder="ACME"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Subdomain
                    </label>
                    <div className="flex items-center">
                      <input
                        type="text"
                        name="subdomain"
                        value={formData.subdomain}
                        onChange={handleChange}
                        className="input"
                        placeholder="acme"
                      />
                      <span className="ml-2 text-neutral-500">.hrms.com</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Company Email *
                    </label>
                    <input
                      type="email"
                      name="primary_email"
                      value={formData.primary_email}
                      onChange={handleChange}
                      className="input"
                      placeholder="contact@acme.com"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Phone Number *
                    </label>
                    <input
                      type="tel"
                      name="primary_phone"
                      value={formData.primary_phone}
                      onChange={handleChange}
                      className="input"
                      placeholder="+1234567890"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Website
                    </label>
                    <input
                      type="url"
                      name="website"
                      value={formData.website}
                      onChange={handleChange}
                      className="input"
                      placeholder="https://acme.com"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Address */}
            {step === 2 && (
              <div className="space-y-4">
                <h2 className="text-2xl font-semibold mb-4">Company Address</h2>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Address Line 1 *
                    </label>
                    <input
                      type="text"
                      name="address_line1"
                      value={formData.address_line1}
                      onChange={handleChange}
                      className="input"
                      placeholder="123 Business Street"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Address Line 2
                    </label>
                    <input
                      type="text"
                      name="address_line2"
                      value={formData.address_line2}
                      onChange={handleChange}
                      className="input"
                      placeholder="Suite 100"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-2">
                        City *
                      </label>
                      <input
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleChange}
                        className="input"
                        placeholder="San Francisco"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-2">
                        State/Province
                      </label>
                      <input
                        type="text"
                        name="state"
                        value={formData.state}
                        onChange={handleChange}
                        className="input"
                        placeholder="California"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-2">
                        Country *
                      </label>
                      <input
                        type="text"
                        name="country"
                        value={formData.country}
                        onChange={handleChange}
                        className="input"
                        placeholder="United States"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-neutral-700 mb-2">
                        Postal Code
                      </label>
                      <input
                        type="text"
                        name="postal_code"
                        value={formData.postal_code}
                        onChange={handleChange}
                        className="input"
                        placeholder="94105"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Admin Information */}
            {step === 3 && (
              <div className="space-y-4">
                <h2 className="text-2xl font-semibold mb-4">Admin Account</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      name="admin_first_name"
                      value={formData.admin_first_name}
                      onChange={handleChange}
                      className="input"
                      placeholder="John"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      name="admin_last_name"
                      value={formData.admin_last_name}
                      onChange={handleChange}
                      className="input"
                      placeholder="Doe"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      name="admin_email"
                      value={formData.admin_email}
                      onChange={handleChange}
                      className="input"
                      placeholder="john.doe@acme.com"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-2">
                      Phone
                    </label>
                    <input
                      type="tel"
                      name="admin_phone"
                      value={formData.admin_phone}
                      onChange={handleChange}
                      className="input"
                      placeholder="+1234567890"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 4: Subscription & Review */}
            {step === 4 && (
              <div className="space-y-6">
                <h2 className="text-2xl font-semibold mb-4">
                  Choose Your Plan
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {[
                    {
                      value: "BASIC",
                      name: "Basic",
                      price: "$29",
                      employees: "50",
                    },
                    {
                      value: "PROFESSIONAL",
                      name: "Professional",
                      price: "$99",
                      employees: "200",
                    },
                    {
                      value: "ENTERPRISE",
                      name: "Enterprise",
                      price: "Custom",
                      employees: "Unlimited",
                    },
                  ].map((plan) => (
                    <label
                      key={plan.value}
                      className={`card cursor-pointer transition-all ${
                        formData.subscription_plan === plan.value
                          ? "border-2 border-primary shadow-soft-lg"
                          : "border-2 border-transparent"
                      }`}
                    >
                      <input
                        type="radio"
                        name="subscription_plan"
                        value={plan.value}
                        checked={formData.subscription_plan === plan.value}
                        onChange={handleChange}
                        className="sr-only"
                      />
                      <div className="text-center">
                        <h3 className="text-xl font-semibold mb-2">
                          {plan.name}
                        </h3>
                        <p className="text-3xl font-bold text-primary mb-2">
                          {plan.price}
                        </p>
                        <p className="text-sm text-neutral-600">
                          Up to {plan.employees} employees
                        </p>
                      </div>
                    </label>
                  ))}
                </div>

                <div className="flex items-start">
                  <input
                    type="checkbox"
                    name="accept_terms"
                    checked={formData.accept_terms}
                    onChange={handleChange}
                    className="mt-1 mr-2"
                    required
                  />
                  <label className="text-sm text-neutral-700">
                    I agree to the{" "}
                    <Link
                      href="/terms"
                      className="text-primary hover:underline"
                    >
                      Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link
                      href="/privacy"
                      className="text-primary hover:underline"
                    >
                      Privacy Policy
                    </Link>
                  </label>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
                {error}
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              {step > 1 && (
                <button
                  type="button"
                  onClick={handleBack}
                  className="btn btn-ghost"
                  disabled={loading}
                >
                  Back
                </button>
              )}

              <div className="ml-auto">
                {step < 4 ? (
                  <button
                    type="button"
                    onClick={handleNext}
                    className="btn btn-primary"
                  >
                    Next
                  </button>
                ) : (
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? (
                      <span className="flex items-center">
                        <div
                          className="spinner mr-2"
                          style={{ width: "20px", height: "20px" }}
                        />
                        Creating Account...
                      </span>
                    ) : (
                      "Create Account"
                    )}
                  </button>
                )}
              </div>
            </div>
          </form>

          {/* Login Link */}
          <div className="mt-6 text-center text-sm text-neutral-600">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="text-primary font-medium hover:underline"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
