import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn, formatUtcDate } from "@/lib/utils";
import { CalendarIcon } from "@radix-ui/react-icons";
import { format } from "date-fns";
import Calendar, { OnClickFunc } from "react-calendar";
import { ptBR } from 'date-fns/locale';
import "react-calendar/dist/Calendar.css";
import React, { useState } from "react";
import { Input } from "./ui/input";
/**
 * exemplo
 *  <InputDate name="data_temp" setValue={form.setValue} />
 * @param param0 
 * @returns 
 */
export default function InputDate({
  name,
  model,
  setValue,
  onClickDay
}: {
  name: string;
  model: any;
  setValue: any;
  onClickDay: OnClickFunc | undefined;
}) {
  const [date, setDate] = useState(model && formatUtcDate(new Date(model)) || new Date());

  // Função para formatar a data
  function formatDate(date:any){
    return format(formatUtcDate(date), 'dd-MM-yyyy', { locale: ptBR });
  };
  return (
    <Popover>
      <div className="flex gap-2">
        <PopoverTrigger asChild>
          <CalendarIcon className="ml-2 mt-2 h-6 w-6 opacity-50 hover:cursor-pointer" />
        </PopoverTrigger>
        <Input
          name={name}
          value={date && formatDate(date)}
          size={8}
          placeholder="dd-mm-yyyy"
          onChange={(val) => {
            if (val.target.value?.length <= 10) {
              setDate(undefined);
              setValue(undefined)
              return;
            }
            if (val.target.value?.length === 0) {
              setDate(undefined);
              setValue(undefined)
              return;
            }
            //setValue(val.toISOString().substring(0, 10))
          }}
          className={cn(
            "w-[110px] pl-3 text-left font-normal",
            !date && "text-muted-foreground",
          )}
        />
      </div>
      <PopoverContent className="w-auto p-0" align="start">
      <Calendar
          onChange={(val:any) => {
            setDate(formatUtcDate(val));
          }}
          onClickDay={onClickDay}
          value={date}
          locale="pt-BR"
          className={"shadow-2xl"}
        />
      </PopoverContent>
    </Popover>
  );
}
