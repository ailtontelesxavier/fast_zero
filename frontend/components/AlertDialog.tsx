import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

import { Button } from "@/components/ui/button";
import { Trash2Icon } from "lucide-react";

export default function AlertDialogComp({
  title,
  description,
  param,
  acao,
}: {
  title: string;
  description: string;
  param: any;
  acao: Function;
}) {
  function setOpenChange(open: boolean) {
    console.log(open);
  }
  return (
    <AlertDialog onOpenChange={setOpenChange}>
      <AlertDialogTrigger asChild>
        <Button variant={"outline"} type="button" size={"sm"} title="excluir">
          <Trash2Icon className="h-4 w-4" />
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancelar</AlertDialogCancel>
          <AlertDialogAction onClick={() => acao(param)}>
            Continue
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
