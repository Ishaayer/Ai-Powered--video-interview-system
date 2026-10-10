import { z } from "zod";


export const resumeSchema = z.object({

  file: z
    .any()
    .refine(
      (file) =>
        file instanceof File,
      "Resume file is required"
    )
    .refine(
      (file) =>
        file?.type === "application/pdf",
      "Only PDF files are allowed"
    )
});


export type ResumeFormData =
  z.infer<typeof resumeSchema>;