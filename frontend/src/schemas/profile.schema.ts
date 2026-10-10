import { z } from "zod";

export const profileSchema = z.object({
  full_name: z
    .string()
    .min(3, "Name must be at least 3 characters"),

  email: z
    .string()
    .email("Invalid email"),

  phone: z
    .string()
    .optional(),

  bio: z
    .string()
    .optional(),
});


export type ProfileFormData =
  z.infer<typeof profileSchema>;