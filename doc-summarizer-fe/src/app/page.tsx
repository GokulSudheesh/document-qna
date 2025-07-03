import { listSessionsApiV1SessionListGet, Session } from "@/client";
import Chat from "@/sections/Chat";

const getSessions = async (): Promise<Session[]> => {
  const data = await listSessionsApiV1SessionListGet();
  return data?.data?.data || [];
};

export default async function Home() {
  const sessions = await getSessions();
  return <Chat initialDataSessions={sessions} />;
}
