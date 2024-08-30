"use client";
import React, { useCallback, useEffect } from "react";
import { useSession } from "next-auth/react";
import { useState } from "react";
import { Icons } from "@/components/icons";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { formatarMoeda } from "@/lib/utils";

export function CardResumoNegociacao({ title, getDados, onClick }: { title: String, getDados: Function, onClick: any }) {
    const [page, setPage] = useState<number>(1);
    const [loading, setLoading] = useState(false);
    const [isBusca, setIsBusca] = useState(true);
    const [total_parcelas, setTotal_parcelas] = useState(null);
    const [total_val_parcela, setTotal_val_parcela] = useState(null);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    useEffect(() => {
        if (isBusca) {
            if (typeof getDados === "function") {
                Obter();
            }
        }
        setIsBusca(false);
        async function Obter() {
            try {
                setLoading(true);
                await getDados(page).then((response: any) => {
                    setTotal_val_parcela(response.data.total_val_parcela);
                    setTotal_parcelas(response.data.total_records);
                }).catch((error: any) => {
                    const responseObject = JSON.parse(error.request.response)
                    var errors = ''
                    responseObject.detail.forEach((val: any) => {
                        errors += (`(Campo: ${val.loc[1]} Erro: ${val.msg}) `)
                    });
                });

            } catch (error: any) {
                if (error.response) {
                    setError(error.response.data.detail + "; " + error.message);
                }
            } finally {
                setLoading(false);
            }
        }
    }, [setTotal_parcelas, setTotal_val_parcela, getDados]);

    if (loading)
        return (
            <Card className="shadow-2xl hover:cursor-pointer">
                <CardContent>
                    <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                </CardContent>
            </Card>);

    return (
        <Card className="shadow-lg hover:cursor-pointer" onClick={onClick}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                    {title}
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">
                    {total_val_parcela}
                </div>
                <p className="text-xs text-muted-foreground">
                    Qtd Parcelas: {total_parcelas}
                </p>
            </CardContent>
        </Card>
    )
}

export default CardResumoNegociacao