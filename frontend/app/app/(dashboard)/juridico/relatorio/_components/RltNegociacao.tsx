"use client";

import { Icons } from "@/components/icons";
import generatePDF from "./generator-pdf-negociacao";
import generatePdfParcelamento from "./generator-pdf-parcelamento";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";

import React, { FormEvent, useEffect, useState } from "react";
import "react-calendar/dist/Calendar.css";
import InputDateForm from "@/components/input-data-form";
import { useSession } from "next-auth/react";
import api from "@/lib/api";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";
import { Label } from "@/components/ui/label";
import { parseJSON } from "date-fns";

const FormSchema = z.object({
    data_inicial: z.date({
        required_error: "Data inicial requerida.",
    }),
    data_final: z.date({
        required_error: "Data final requerida.",
    }),
    data_temp: z
        .date({
            required_error: "Data temp requerida.",
        })
        .optional(),
    tipo: z.string(),
});

export default function RltNegociacao() {
    const { data: session, status } = useSession();
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [data_inicial, setData_inicial] = useState("");
    const [data_final, setData_final] = useState("");
    const [tipo, setTipo] = useState("");

    const [loading, setLoading] = useState(true);

    var _session: any = session;

    useEffect(() => {
        setLoading(false);
    }, []);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();
        const formData = new FormData(event.target as HTMLFormElement);
        //if (!(formData.get("tipo") as String).trim()) {
        if (!(tipo as String).trim()) {
            setError("Selecione o tipo de relatorio");
            return;
        }
        if (!(formData.get("data_inicial") as String).trim()) {
            setError("Selecione a data inicial");
            return;
        }
        if (!(formData.get("data_final") as String).trim()) {
            setError("Selecione a data final");
            return;
        }
        setLoading(true);
        const response = await rltNegociacao(formData);
        //console.log(response)
        switch (formData.get('tipo')) {
            case "1":
                generatePDF(response, _session?.sub);
                break;
            case "2":
                generatePdfParcelamento(response, _session?.sub);
                break;
        }
        setLoading(false);
    }

    return (
        <div>
            <h1>{">>"}Negociação</h1>
            <div className="flex gap-2 mt-2">
                <form onSubmit={handleSubmit} className="space-y-8">
                    <div className="flex flex-row items-center justify-center gap-4 mt-4">
                        <div className="">
                            <Label>Tipo Relatorio</Label>
                            <Select name="tipo" onValueChange={setTipo} defaultValue={tipo}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Selecione o relatorio" />
                                </SelectTrigger>
                                <SelectContent className="text-black">
                                    <SelectItem value="1">Negociação Por Período</SelectItem>
                                    <SelectItem value="2">Parcelas Por Período</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2 w-44">
                            <Label htmlFor="data_inicial">Data Inicial</Label>
                            <InputDateForm
                                className={"w-full"}
                                field={data_inicial}
                                onClickDay={handleChangeDataInicial}
                            />
                            <input
                                hidden={true}
                                name="data_inicial"
                                value={data_inicial ?? null}
                            />
                        </div>
                        <div className="space-y-2 w-44">
                            <Label htmlFor="data_final">Data Inicial</Label>
                            <InputDateForm
                                className={"w-full"}
                                field={data_final}
                                onClickDay={handleChangeDataFinal}
                            />
                            <input
                                hidden={true}
                                name="data_final"
                                value={data_final ?? null}
                            />
                        </div>
                    </div>
                    <div className="col-span-12">
                        {success && (
                            <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
                        )}
                        {error && (
                            <AlertDestructive setError={setError}>{error}</AlertDestructive>
                        )}
                    </div>

                    <div className="col-span-12 flex justify-end">
                        <Button className="" type="submit">
                            {loading && (
                                <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                            )}
                            Gerar
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );

    async function rltNegociacao(formData: any) {
        const stringFormatada = Array.from(formData.entries())
            .map(([key, value]) => `${key}=${encodeURIComponent("" + value)}`)
            .join("&");
        var result: any = []
        try {
            setLoading(true);
            await api
                .get(`/juridico/negociacao/relatorio/?${stringFormatada}`)
                .then((response) => {
                    result = response.data;
                })
                .catch((error) => {
                    const responseObject = JSON.parse(error.request.response);
                    var errors = "";
                    responseObject.detail.forEach((val: any) => {
                        errors += `(Campo: ${val.loc[1]} Erro: ${val.msg}) `;
                    });
                });
        } catch (error: any) {
            if (error.response) {
                setError(error.response.data.detail + "; " + error.message);
            }
        } finally {
            setLoading(false);
        }
        return result
    }

    function handleChangeDataInicial(value: any) {
        setData_inicial(value.toISOString().substring(0, 10));
    }
    function handleChangeDataFinal(value: any) {
        setData_final(value.toISOString().substring(0, 10));
    }
}
