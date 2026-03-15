import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { SectionHeading } from "@/components/section-heading";

describe("SectionHeading component", () => {
  it("renders the title", () => {
    render(<SectionHeading title="My Projects" />);
    expect(screen.getByText("My Projects")).toBeInTheDocument();
  });

  it("renders the subtitle when provided", () => {
    render(<SectionHeading title="Experience" subtitle="Where I have worked" />);
    expect(screen.getByText("Where I have worked")).toBeInTheDocument();
  });

  it("does not render a subtitle element when subtitle is omitted", () => {
    render(<SectionHeading title="Skills" />);
    expect(screen.queryByRole("paragraph")).not.toBeInTheDocument();
  });

  it("renders the title as an h2", () => {
    render(<SectionHeading title="About Me" />);
    expect(screen.getByRole("heading", { level: 2, name: "About Me" })).toBeInTheDocument();
  });
});
