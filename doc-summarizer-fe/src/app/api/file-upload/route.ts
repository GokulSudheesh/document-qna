import { NextResponse, NextRequest } from "next/server";
import path from "path";
import { writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const POST = async (req: NextRequest, _res: NextResponse) => {
  try {
    const formData = await req.formData();

    const file = formData.get("file") as File;
    if (!file) {
      return NextResponse.json(
        { error: "No files received." },
        { status: 400 }
      );
    }

    const buffer = Buffer.from(await file.arrayBuffer());
    const filename = file.name.replaceAll(" ", "_");
    console.log(filename);
    const cwd = process.cwd();
    const directoryPath = path.join(cwd, "public/fileUploads");

    if (!existsSync(directoryPath)) {
      await mkdir(directoryPath, { recursive: true });
    }

    await writeFile(
      path.join(process.cwd(), "public/fileUploads/" + filename),
      buffer
    );
    return NextResponse.json(
      {
        success: true,
        data: { message: "File uploaded successfully." },
      },
      { status: 201 }
    );
  } catch (error) {
    console.log("Error occured ", error);
    return NextResponse.json(
      {
        success: false,
        data: { message: "Internal Server Error" },
      },
      { status: 500 }
    );
  }
};
