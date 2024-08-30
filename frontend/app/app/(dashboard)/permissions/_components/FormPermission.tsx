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
import { useRouter } from "next/navigation";
import { Textarea } from "@/components/ui/textarea";
import ComboboxModule from "./ComboboxModule";

export default function FormPermission({ id, setIsBusca }: { id: number, setIsBusca: Function }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [selectOption, setSelectOption] = useState("");
  const [permission, setPermission] = useState<any>({});
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

  function handlePermission(event: FormEvent) {
    event.preventDefault();

    if (permission.name.length < 3) {
      setError("O nome deve ter pelo menos 3 caracteres");
      return;
    }

    if(id){
      updatePermission();
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
      // busca permissions ao fechar modal
      setIsBusca(true);
      return;
    }

    if (id) {
      getPermission();
    }

    async function getPermission() {
      await api.get(`/permissoes/permission/${id}`).then((response) => {
        console.log(response);
        setPermission(response.data);
      });
    }
  }, [id, modalIsOpen, setIsBusca]);

  async function create() {
    try {
      await api
        .post("/permissoes/permission/", {
          name: permission.name,
          module_id: permission.module_id,
          description: permission.description
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

  async function updatePermission() {
    try {
      await api
        .put("/permissoes/permission/"+id, {
          id: id,
          module_id: permission.module_id,
          name: permission.name,
          description: permission.description
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
            <DialogTitle>Cadastro de Permission</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <form onSubmit={handlePermission}>
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
                      value={permission.id ?? ""}
                    />
                  </>
                )}
                <Label htmlFor="name" className="text-right">
                  Nome
                </Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Nome"
                  className="col-span-3"
                  value={permission.name ?? ""}
                  onChange={(e) =>
                    setPermission({ ...permission, name: e.target.value })
                  }
                />
                <Label className="text-right">
                  Modulo
                </Label>
                <div className="w-64">
                  <ComboboxModule objeto={permission} />
                </div>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="description" className="text-right">
                  Descricao
                </Label>
                <Textarea
                  id="description"
                  placeholder="Nome"
                  className="col-span-3"
                  value={permission.description ?? ""}
                  onChange={(e:any) =>
                    setPermission({ ...permission, description: e.target.value })
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
