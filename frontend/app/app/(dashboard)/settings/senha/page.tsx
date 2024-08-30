"use client";

import { useState, useMemo, useEffect, FormEvent } from "react";
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter,
} from "@/components/ui/card";
import api from "@/lib/api";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { AxiosHeaders, AxiosRequestConfig } from "axios";

export default function Page() {
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const [oldpassword, setOldPassword] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");

    function handleSenha(event: FormEvent) {
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
        console.log()

        savePassword();
    }

    async function savePassword() {
        const config: AxiosRequestConfig = {
            password: oldpassword,
            new_password: password,
            //headers:  new AxiosHeaders().setContentType("application/x-www-form-urlencoded"),
        };
        try {
            await api
                .put("/users/update-password/", config)
                .then((response) => {
                    setSuccess(response.data)
                })
                .catch((error) => {
                    const responseObject = JSON.parse(error.request.response);
                    var errors = "";
                    responseObject.detail.forEach((val: any) => {
                        errors += `(Campo: ${val.loc[1]} Erro: ${val.msg}) `;
                    });
                });
        } catch (error) {
        } finally {
        }
    }

    return (
        <Card className="w-full max-w-4xl">
            <CardHeader>
                <CardTitle>Gerenciar Senha</CardTitle>
                <CardDescription>Altera senha de usuario logado</CardDescription>
            </CardHeader>
            <form onSubmit={handleSenha}>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <Label htmlFor="password">Senha Atual</Label>
                            <Input
                                type="password"
                                placeholder="Senha"
                                value={oldpassword}
                                onChange={(event) => setOldPassword(event.target.value)}
                            />
                        </div>
                        <div>
                            <Label htmlFor="password">Nova Senha</Label>
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
                </CardContent>
                <CardFooter>
                    <div className="flex w-full items-end justify-end gap-4">
                        <Button
                            type="button"
                            variant={"secondary"}
                        >
                            Limpar
                        </Button>
                        <Button
                            type="submit"
                            variant={"default"}
                        >
                            Salvar
                        </Button>
                    </div>
                    <section className="w-full">
                        {success && (
                            <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
                        )}
                        {error && (
                            <AlertDestructive setError={setError}>{error}</AlertDestructive>
                        )}
                    </section>
                </CardFooter>
            </form>
        </Card>
    );
}
