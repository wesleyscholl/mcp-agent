import { Octokit } from "octokit";
import dotenv from "dotenv";

dotenv.config();

export const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

export async function createPullRequest({ repoUrl, branch, base, title, body }) {
  const [_, owner, repo] = new URL(repoUrl).pathname.split("/");

  const pr = await octokit.request("POST /repos/{owner}/{repo}/pulls", {
    owner,
    repo,
    head: branch,
    base,
    title,
    body,
  });

  return pr.data.html_url;
}