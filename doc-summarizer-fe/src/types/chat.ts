import { EventSourceMessage } from "@microsoft/fetch-event-source";
import { Reference } from "@/client/types.gen";

export type TChatState = "loading" | "stream" | undefined;

export interface ChatState {
  sessionId: string;
  status: TChatState;
}

export type ChatSSEEvent = EventSourceMessage &
  (
    | {
        event: "message";
        data: {
          id: string;
          message: string;
        };
      }
    | {
        event: "references";
        data: {
          id: string;
          references: Reference[] | null;
        };
      }
  );
