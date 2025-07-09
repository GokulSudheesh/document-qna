import { listSessionsApiV1SessionListGet, Session } from "@/client";
import Chat from "@/sections/Chat";

const getSessions = async (): Promise<Session[]> => {
  try {
    const data = await listSessionsApiV1SessionListGet();
    return data?.data?.data || [];
  } catch (error) {
    console.error("Failed to fetch sessions:", error);
    return [];
  }
};

export default async function Home() {
  const sessions = await getSessions();
  return <Chat initialDataSessions={sessions} />;
}
