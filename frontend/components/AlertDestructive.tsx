import { ExclamationTriangleIcon, Cross1Icon } from "@radix-ui/react-icons";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import React, { useState } from "react";
import { cn } from "../lib/utils";

interface AlertDestructiveProps {
  children: React.ReactNode;
  setError: Function;
}

export function AlertDestructive({ children, setError }: AlertDestructiveProps) {
  return (
    <Alert variant="destructive" /* className={cn("", { hidden: isHidden })} */>
      <ExclamationTriangleIcon className="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <div className="flex w-full -mt-4 justify-end items-end">
        <Cross1Icon
          className="h-4 w-4 hover:cursor-pointer"
          onClick={() => setError("")}
        />
      </div>
      <AlertDescription>{children}</AlertDescription>
    </Alert>
  );
}
