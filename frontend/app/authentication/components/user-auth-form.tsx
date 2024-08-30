"use client";

import * as React from "react";
import { useState } from "react";

import { cn } from "@/lib/utils";
import { Icons } from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form } from "@/components/ui/form";

import { ExclamationTriangleIcon } from "@radix-ui/react-icons";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  FormControl,
  FormField,
  FormLabel,
  FormItem,
  FormDescription,
  FormMessage,
} from "@/components/ui/form";
import { signIn, signOut } from "next-auth/react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { unstable_noStore as noStore } from "next/cache";

const formSchema = z.object({
  username: z.string().min(5),
  password: z.string({
    required_error: "Senha requerida.",
  }),
  client_secret: z.string().max(6).min(6)
});

type LoginFormData = z.infer<typeof formSchema>;

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export const dynamic = 'force-dynamic';

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const form = useForm<LoginFormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
      client_secret: "",
    },
  });

  const [ms_error, setMs_error] = useState("");

  const onSubmit = async (values: LoginFormData) => {
    const resp = await signIn("credentials", { redirect: false, ...values });
    if (!resp?.ok) {
      setMs_error("Erro verifique usuario e senha.");
    } else {
      setMs_error("");
    }
  };

  const router = useRouter();
  const { data: session, update, status } = useSession();

  React.useEffect(() => {
    //console.log("session: ", session);
    if (status === "authenticated") {
      router.push("/app");
    }
  }, [status, router]);

  return (
    <div className={cn("grid gap-4", className)} {...props}>
      <div className="flex w-full mt-10 items-center flex-col gap-3">
        <div className="relative z-10">
          <Form {...form}>
            <form
              action="#"
              className="w-96"
              onSubmit={form.handleSubmit(onSubmit)}
              hidden={status === "loading"}
            >
              <div className="text-black mb-6">
                <FormField
                  control={form.control}
                  name="username"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-start">
                        Usuario
                      </FormLabel>
                      <FormControl>
                        <Input
                          placeholder="usuario"
                          type="text"
                          {...field}
                          className="text-black"
                        />
                      </FormControl>
                      <FormDescription></FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className="text-black mb-6">
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-start">Senha</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Senha"
                          type="password"
                          {...field}
                          className="text-black"
                        />
                      </FormControl>
                      <FormDescription></FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className="text-black mb-6">
                <FormField
                  control={form.control}
                  name="client_secret"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-start">
                        Secret
                      </FormLabel>
                      <FormControl>
                        <Input
                          placeholder="secret"
                          type="text"
                          {...field}
                          className="text-black"
                        />
                      </FormControl>
                      <FormDescription></FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            </form>
          </Form>
          {ms_error && (
            <Alert variant="destructive">
              <ExclamationTriangleIcon className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                {ms_error}
              </AlertDescription>
            </Alert>
          )}
        </div>
        <Button
          onClick={form.handleSubmit(onSubmit)}
          className="py-1"
          variant={"outline"}
          size={"lg"}
          disabled={status === "loading"}
        >
          {status === "loading" ? (
            <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            ""
          )}{" "}
          <span>Acessar</span>
        </Button>
      </div>
    </div>
  );
}
