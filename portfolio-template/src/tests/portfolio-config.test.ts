import { describe, it, expect } from "vitest";
import { portfolio } from "@/config/portfolio";

describe("portfolio config", () => {
  it("has required top-level fields", () => {
    expect(portfolio.name).toBeTruthy();
    expect(portfolio.title).toBeTruthy();
    expect(portfolio.bio).toBeTruthy();
    expect(portfolio.email).toBeTruthy();
    expect(portfolio.location).toBeTruthy();
    expect(portfolio.resumeUrl).toBeTruthy();
  });

  it("has at least one social link with required fields", () => {
    expect(portfolio.socials.length).toBeGreaterThan(0);
    for (const social of portfolio.socials) {
      expect(social.platform).toBeTruthy();
      expect(social.url).toBeTruthy();
      expect(social.icon).toBeTruthy();
    }
  });

  it("has at least one project with required fields", () => {
    expect(portfolio.projects.length).toBeGreaterThan(0);
    for (const project of portfolio.projects) {
      expect(project.title).toBeTruthy();
      expect(project.description).toBeTruthy();
      expect(project.tags.length).toBeGreaterThan(0);
    }
  });

  it("has at least one experience entry with required fields", () => {
    expect(portfolio.experience.length).toBeGreaterThan(0);
    for (const exp of portfolio.experience) {
      expect(exp.company).toBeTruthy();
      expect(exp.role).toBeTruthy();
      expect(exp.startDate).toBeTruthy();
      expect(exp.endDate).toBeTruthy();
      expect(exp.description.length).toBeGreaterThan(0);
    }
  });

  it("has at least one skill category with skills", () => {
    expect(portfolio.skills.length).toBeGreaterThan(0);
    for (const category of portfolio.skills) {
      expect(category.name).toBeTruthy();
      expect(category.skills.length).toBeGreaterThan(0);
    }
  });

  it("has about section with description and highlights", () => {
    expect(portfolio.about.description.length).toBeGreaterThan(0);
    expect(portfolio.about.highlights.length).toBeGreaterThan(0);
    for (const highlight of portfolio.about.highlights) {
      expect(highlight.label).toBeTruthy();
      expect(highlight.value).toBeTruthy();
    }
  });

  it("email is a valid email address format", () => {
    expect(portfolio.email).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  });
});
