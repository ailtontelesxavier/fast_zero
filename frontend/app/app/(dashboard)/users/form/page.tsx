"use client";
import { FormEvent, useState } from "react";
import PageTitle from "@/components/PageTitle";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { AlertDestructive } from "@/components/AlertDestructive";
import { AlertSuccess } from "@/components/AlertSuccess";
import { useRouter } from "next/navigation";

export default function UserFormPage() {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  function handleCreateUser(event: FormEvent) {
    event.preventDefault();

    // Regex para verificar se a senha contém pelo menos uma letra maiúscula e um caractere especial
    const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])/;

    if (password !== password2) {
      setError("As senhas não coincidem");
      return;
    }

    if (password === "" || password2 === "") {
      setError("A senha não pode estar vazia");
      return;
    }

    if (password.length < 6) {
      setError("A senha deve ter pelo menos 6 caracteres");
      return;
    }

    if (!passwordRegex.test(password)) {
      setError(
        "A senha deve conter pelo menos uma letra maiúscula e um caractere especial"
      );
      return;
    }

    saveUser();
    setError("");
  }

  async function saveUser() {
    try {
      await api
        .post("/users/", {
          username: username,
          email: email,
          password: password,
        })
        .then((response: any) => {
          if (response.status === 201) {
            setSuccess("Cadastrado com sucesso");
            limparForm();
          }
        }).catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  function limparForm() {
    setUsername("");
    setEmail("");
    setPassword("");
    setPassword2("");
  }
  return (
    <div className="flex flex-col gap-5  w-full">
      <PageTitle title="Cadastro de Usuario" />
      <section>
        <form onSubmit={handleCreateUser}>
          <div className="flex flex-col gap-2 md:grid grid-cols-2">
            <div>
              <Label htmlFor="username">Usuario</Label>
              <Input
                id="username"
                type="text"
                placeholder="Usuario"
                required={true}
                value={username}
                onChange={(event) => setUsername(event.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="email"
                required={true}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="password">Senha</Label>
              <Input
                type="password"
                placeholder="Senha"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="password2">Confirme a Senha</Label>
              <Input
                id="password2"
                type="password"
                placeholder="Senha"
                value={password2}
                onChange={(event) => setPassword2(event.target.value)}
              />
            </div>
          </div>
          <div className="flex mt-5 gap-4 w-full justify-end">
            <Button type="button" variant={"secondary"} onClick={()=>router.push('/app/users/')}>Cancelar</Button>
            <Button type="button" variant={"secondary"} onClick={()=>limparForm()}>Limpar</Button>
            <Button type="submit">Cadastrar</Button>
          </div>
        </form>
      </section>
      <section>
        {success && <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>}
        {error && <AlertDestructive setError={setError}>{error}</AlertDestructive>}
      </section>
    </div>
  );
}
