"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FormEvent, useEffect, useState } from "react";
import { PlusIcon, Pencil2Icon } from "@radix-ui/react-icons";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";

export default function FormModule({ id, setIsBusca }: { id: number, setIsBusca: Function }) {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [selectOption, setSelectOption] = useState("");
  const [module, setModule] = useState<any>({});
  const [modalIsOpen, setModalIsOpen] = useState(false);

  function hangleOnValueChange(value: string) {
    setSelectOption(value);
  }

  function openModal() {
    if (selectOption) {
      setModalIsOpen(true);
    }
  }

  function closeModal() {
    setModalIsOpen(false);
  }

  function handleModule(event: FormEvent) {
    event.preventDefault();

    if (module.title.length < 3) {
      setError("O nome deve ter pelo menos 3 caracteres");
      return;
    }

    if(id){
      updateModule();
      setIsBusca(true);
      setError("");
      return;
    }
    create();
    setIsBusca(true);
    setError("");
  }

  useEffect(() => {
    if (!modalIsOpen) {
      // busca perfils ao fechar modal
      setIsBusca(true);
      return;
    }

    if (id) {
      getModule();
    }

    async function getModule() {
      await api.get(`/permissoes/module/${id}`).then((response) => {
        console.log(response);
        setModule(response.data);
      });
    }
  }, [id, modalIsOpen, setIsBusca]);

  async function create() {
    try {
      await api
        .post("/permissoes/module/", {
          title: module.title,
        })
        .then((response: any) => {
          if (response.status === 201) {
            setSuccess("Cadastrado com sucesso");
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  async function updateModule() {
    try {
      await api
        .put("/permissoes/module/"+id, {
          id: id,
          title: module.title,
        })
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Atualizado com sucesso");
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  function setOpenChange(open: boolean) {
    setModalIsOpen(open)
  }

  return (
    <div className="flex gap-2">
      <Dialog open={modalIsOpen} onOpenChange={setOpenChange}>
        <DialogTrigger asChild>
          <Button
            variant={"outline"}
            type="button"
            size={"sm"}
            title={id ? "editar" : "adicionar modulo"}
            onClick={() => setModalIsOpen(true)}
          >
            {id ? (
              <Pencil2Icon className="h-4 w-4" />
            ) : (
              <PlusIcon className="h-4 w-4" />
            )}
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Cadastro de Modulo</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <form onSubmit={handleModule}>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                {id > 0 && (
                  <>
                    <Label htmlFor="id" className="text-right">
                      ID
                    </Label>
                    <Input
                      id="id"
                      type="text"
                      placeholder="id"
                      className="col-span-3"
                      disabled={true}
                      value={module.id ?? ""}
                    />
                  </>
                )}
                <Label htmlFor="title" className="text-right">
                  Nome
                </Label>
                <Input
                  id="title"
                  type="text"
                  placeholder="Nome"
                  className="col-span-3"
                  value={module.title ?? ""}
                  onChange={(e) =>
                    setModule({ ...module, title: e.target.value })
                  }
                />
              </div>
            </div>
            <div className="flex items-end justify-end gap-2">
              <Button
                type="button"
                variant={"secondary"}
                onClick={() => closeModal()}
              >
                Cancelar
              </Button>
              <Button type="submit">Salvar</Button>
            </div>
          </form>
          <DialogFooter>
            <section className="w-full">
              {success && (
                <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
              )}
              {error && (
                <AlertDestructive setError={setError}>{error}</AlertDestructive>
              )}
            </section>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
