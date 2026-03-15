import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Footer } from "@/components/footer";
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
    description: ["About me."],
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

describe("Footer component", () => {
  it("renders the developer name in the copyright line", () => {
    render(<Footer profile={mockProfile} />);
    expect(screen.getByText(/Jane Doe/)).toBeInTheDocument();
  });

  it("renders the current year in the copyright line", () => {
    render(<Footer profile={mockProfile} />);
    const year = new Date().getFullYear().toString();
    expect(screen.getByText(new RegExp(year))).toBeInTheDocument();
  });

  it("renders social icon links with correct hrefs", () => {
    render(<Footer profile={mockProfile} />);
    const githubLink = screen.getByRole("link", { name: "GitHub" });
    expect(githubLink).toHaveAttribute("href", "https://github.com/jane");
    const linkedinLink = screen.getByRole("link", { name: "LinkedIn" });
    expect(linkedinLink).toHaveAttribute("href", "https://linkedin.com/in/jane");
  });

  it("social links open in a new tab", () => {
    render(<Footer profile={mockProfile} />);
    const githubLink = screen.getByRole("link", { name: "GitHub" });
    expect(githubLink).toHaveAttribute("target", "_blank");
    expect(githubLink).toHaveAttribute("rel", "noopener noreferrer");
  });
});
