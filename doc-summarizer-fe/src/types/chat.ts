export type TChatState = "loading" | "stream" | undefined;

export interface ChatState {
  sessionId: string;
  status: TChatState;
}
