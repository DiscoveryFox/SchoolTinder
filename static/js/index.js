export class MatchClient {
  constructor(baseUrl = "/match") {
    this.baseUrl = baseUrl;
  }

  // GET /match → get next match
  async getNextMatch() {
    const res = await fetch(this.baseUrl, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    if (!res.ok) {
      throw new Error(`Failed to get match (${res.status})`);
    }

    return await res.json();
  }

  // POST /match → update match (success / denial)
  async updateMatch(otherProfileId, result) {
    if (result !== "success" && result !== "denial") {
      throw new Error("result must be 'success' or 'denial'");
    }

    const res = await fetch(this.baseUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        otherProfileId,
        result
      })
    });

    if (!res.ok) {
      throw new Error(`Failed to update match (${res.status})`);
    }

    return await res.json();
  }
}
