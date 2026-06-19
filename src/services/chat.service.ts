// chat.service.ts

export interface ChatResponse {
  recruiterTimeBreakdown: {
    title: string;
    description: string;
    metrics: string[];
    opportunities: string[];
  };
  benchmark: {
    title: string;
    description: string;
  };
}

const API_BASE_URL = "/api/chat"; // later  will replace this

export const fetchDashboardData = async (): Promise<ChatResponse> => {
  try {
    // Later replace this with real endpoint
    // const response = await fetch(`${API_BASE_URL}/dashboard`);
    // return await response.json();

    // Dummy Response (for now)
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          recruiterTimeBreakdown: {
            title: "Recruiter Time Breakdown",
            description:
              "The market is projected to reach $12.8B by 2026, driven by demandfor cost optimization, 24/7 availability, and personalized customerexperiences, with strategic recommendations varying by organizationsize: enterprises should prioritize omnichannel capabilities andintegration ecosystems, mid-market companies should focus on quickdeployment and personalization, and SMBs should emphasizecost-effective high-automation solutions to maximize ROI",
            metrics: [
              "Average time-to-hire: 45 days (industry avg: 23 days)",
              "Cost per hire: $4,200 (industry avg: $3,100)",
              "Interview-to-offer ratio: 6:1"
            ],
            opportunities: [
              "Resume screening automation",
              "Interview scheduling optimization",
              "Candidate chatbot",
              "Bias reduction analytics"
            ]
          },
          benchmark: {
            title: "Current vs Industry Benchmarks",
            description: "Comparison between internal and industry performance."
          }
        });
      }, 1200);
    });
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};