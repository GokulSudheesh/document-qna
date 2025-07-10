import { deleteSessionApiV1SessionSessionIdDelete } from "@/client";

export const deleteSession = async (sessionId: string) => {
  const { data, response } = await deleteSessionApiV1SessionSessionIdDelete({
    path: { session_id: sessionId },
  });

  if (!(response.ok && data?.success))
    throw new Error(`Error deleting session: ${response.status}`);

  return data;
};
