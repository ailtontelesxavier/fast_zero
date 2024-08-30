import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn, formatUtcDate } from "@/lib/utils";
import { CalendarIcon } from "@radix-ui/react-icons";
import { format } from "date-fns";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import { Button } from "./ui/button";
import React, { useEffect, useState } from "react";
import { ptBR } from "date-fns/locale";

export default function InputDateForm({
  field,
  onClickDay,
  className,
}: {
  field: any;
  onClickDay: any | undefined;
  className?: String | '';
}) {
  const [date, setDate] = useState<any>(field && formatUtcDate(new Date(field)) || new Date());

  useEffect(() => {
    if (field) { 
      setDate(formatUtcDate(field && formatUtcDate(new Date(field)) || new Date()));
    }
  }, [field])

  // Função para formatar a data
  function formatDate(date: any) {
    return format(formatUtcDate(date), 'dd-MM-yyyy', { locale: ptBR });
  };
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-[130px] pl-3 text-left font-normal " + className,
            !field && "text-muted-foreground"
          )}
        >
          {field ? (
            formatDate(date)
          ) : (
            <span>dd-MM-yyyy</span>
          )}
          <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        {onClickDay ? (
          <Calendar
            onChange={(val: any) => {
              setDate(formatUtcDate(val));
            }}
            onClickDay={onClickDay}
            value={date}
            locale="pt-BR"
            className={"shadow-2xl"}
          />
        ) : (
          <Calendar
            onChange={(val: any) => {
              setDate(formatUtcDate(val));
            }}
            value={date}
            locale="pt-BR"
            className={"shadow-2xl"}
          />
        )}
      </PopoverContent>
    </Popover>
  );
}
