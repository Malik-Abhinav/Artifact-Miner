import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Hero } from "@/components/hero";
import type { DeveloperProfile } from "@/types/portfolio";

const mockProfile: DeveloperProfile = {
  name: "Jane Doe",
  title: "Software Engineer",
  bio: "Building great software.",
  avatarUrl: "/avatar.jpg",
  resumeUrl: "/resume.pdf",
  email: "jane@example.com",
  location: "Toronto, ON",
  socials: [
    { platform: "GitHub", url: "https://github.com/jane", icon: "github" },
    { platform: "LinkedIn", url: "https://linkedin.com/in/jane", icon: "linkedin" },
  ],
  about: {
    description: ["About me paragraph."],
    highlights: [{ label: "Years Experience", value: "3+" }],
  },
  skills: [{ name: "Languages", skills: ["TypeScript"] }],
  projects: [
    {
      title: "My Project",
      description: "A cool project.",
      image: "/project.jpg",
      tags: ["React"],
    },
  ],
  experience: [
    {
      company: "Acme Corp",
      role: "Engineer",
      startDate: "Jan 2022",
      endDate: "Present",
      description: ["Built things."],
    },
  ],
};

describe("Hero component", () => {
  it("renders the developer name", () => {
    render(<Hero profile={mockProfile} />);
    expect(screen.getByText("Jane Doe")).toBeInTheDocument();
  });

  it("renders the developer title", () => {
    render(<Hero profile={mockProfile} />);
    expect(screen.getByText("Software Engineer")).toBeInTheDocument();
  });

  it("renders the bio", () => {
    render(<Hero profile={mockProfile} />);
    expect(screen.getByText("Building great software.")).toBeInTheDocument();
  });

  it("renders the location", () => {
    render(<Hero profile={mockProfile} />);
    expect(screen.getByText("Toronto, ON")).toBeInTheDocument();
  });

  it("renders the Resume CTA link pointing to resumeUrl", () => {
    render(<Hero profile={mockProfile} />);
    const resumeLink = screen.getByRole("link", { name: /resume/i });
    expect(resumeLink).toHaveAttribute("href", "/resume.pdf");
  });

  it("renders the Contact CTA link as a mailto", () => {
    render(<Hero profile={mockProfile} />);
    const contactLink = screen.getByRole("link", { name: /contact/i });
    expect(contactLink).toHaveAttribute("href", "mailto:jane@example.com");
  });

  it("renders social icon links with correct aria-labels and hrefs", () => {
    render(<Hero profile={mockProfile} />);
    const githubLink = screen.getByRole("link", { name: "GitHub" });
    expect(githubLink).toHaveAttribute("href", "https://github.com/jane");
    const linkedinLink = screen.getByRole("link", { name: "LinkedIn" });
    expect(linkedinLink).toHaveAttribute("href", "https://linkedin.com/in/jane");
  });

  it("social links open in a new tab", () => {
    render(<Hero profile={mockProfile} />);
    const githubLink = screen.getByRole("link", { name: "GitHub" });
    expect(githubLink).toHaveAttribute("target", "_blank");
    expect(githubLink).toHaveAttribute("rel", "noopener noreferrer");
  });
});
