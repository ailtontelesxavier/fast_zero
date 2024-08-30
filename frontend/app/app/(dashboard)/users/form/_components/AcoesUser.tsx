"use client";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { FormEvent, useState } from "react";
import { PaperPlaneIcon } from "@radix-ui/react-icons";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";

export default function AcoesUser({id}: {id: number}) {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectOption, setSelectOption] = useState("");
  const [user, setUser] = useState<any>({});

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
    limparForm();
  }

  function handleAlterPassword(event: FormEvent) {
    event.preventDefault();

    const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])/;

    console.log("aqui");

    if (user.password !== user.password2) {
      setError("As senhas não coincidem");
      return;
    }

    if (user.password === "" || user.password2 === "") {
      setError("A senha não pode estar vazia");
      return;
    }

    if (user.password.length < 6) {
      setError("A senha deve ter pelo menos 6 caracteres");
      return;
    }

    if (!passwordRegex.test(user.password)) {
      setError(
        "A senha deve conter pelo menos uma letra maiúscula e um caractere especial"
      );
      return;
    }

    save();
    setError("");
  }

  async function save() {
    try {
      await api.put("/users/update-password/"+id, {
            password: user.password,
        }).then((response: any) => {
          if (response.status === 200) {
            setSuccess("Senha atualizada com sucesso");
            limparForm();
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  function limparForm() {
    setUser({});
  }
  return (
    <div className="flex gap-2">
      <Select onValueChange={(value) => hangleOnValueChange(value)}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Selecione uma acao" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Acoes</SelectLabel>
            <SelectItem value="1">Alterar senha</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <Dialog open={modalIsOpen} onOpenChange={setModalIsOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Alterar Senha</DialogTitle>
            <DialogDescription>
              A senha deve conter pelo menos uma letra maiúscula, uma letra
              minuscula e um caractere especial
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleAlterPassword}>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="password" className="text-right">
                  Senha
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="senha"
                  className="col-span-3"
                  value={user.password ?? ""}
                  onChange={(e) => setUser({ ...user, password: e.target.value })}
                  />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="password2" className="text-right">
                  Senha
                </Label>
                <Input
                  id="password2"
                  type="password"
                  value={user.password2 ?? ""}
                  placeholder="senha"
                  onChange={(e) =>
                    setUser({ ...user, password2: e.target.value })
                  }
                  className="col-span-3"
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
      <Button size={"sm"} variant={"outline"} onClick={() => openModal()}>
        <PaperPlaneIcon className="h-4 x-4" />
      </Button>
    </div>
  );
}
