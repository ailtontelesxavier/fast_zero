import { CheckCircledIcon, Cross1Icon } from "@radix-ui/react-icons"

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import { useState } from "react";
import { cn } from "@/lib/utils";

interface AlertSuccessProps{
    children: React.ReactNode;
    setSuccess: Function;
}

export function AlertSuccess({children, setSuccess}: AlertSuccessProps) {

  return (
    <Alert>
      <CheckCircledIcon className="h-4 w-4" />
      <AlertTitle>Ação realizada com sucesso!</AlertTitle>
      <div className="flex w-full -mt-4 justify-end items-end">
        <Cross1Icon
          className="h-4 w-4 hover:cursor-pointer"
          onClick={() => setSuccess("")}
        />
      </div>
      <AlertDescription>
        {children}
      </AlertDescription>
    </Alert>
  )
}
