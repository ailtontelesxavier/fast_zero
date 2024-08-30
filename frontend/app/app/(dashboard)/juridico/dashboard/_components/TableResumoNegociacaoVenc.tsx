"use client";
import { AlertDestructive } from "@/components/AlertDestructive";
import { AlertSuccess } from "@/components/AlertSuccess";
import { Icons } from "@/components/icons";
import { PaginationActionsApi } from "@/components/paginationActionsApi";
import { format, parseISO } from "date-fns";
import { CheckIcon, Cross2Icon } from "@radix-ui/react-icons";
import {
    Table,
    TableHeader,
    TableRow,
    TableHead,
    TableBody,
    TableCell,
    TableFooter,
} from "@/components/ui/table";
import api from "@/lib/api";
import { formatarData, formatUtcDate } from "@/lib/utils";
import { useEffect, useState } from "react";
import { ptBR } from "date-fns/locale";


export function TableResumoNegociacaoVenc({
    title,
    getDados,
}: {
    title: String,
    getDados: Function;
}) {
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState<number>(1);
    const [loading, setLoading] = useState(false);
    const [isBusca, setIsBusca] = useState(true);
    const [parcelamentoLis, setParcelamentoList] = useState([]);

    useEffect(() => {
        if (typeof getDados === "function") {
            Obter();
        }
        async function Obter() {
            try {
                setLoading(true);
                await getDados(page).then((response: any) => {
                    console.log(response.data.rows)
                    setParcelamentoList(response.data.rows);
                    setTotal(response.data.total_records);
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
    }, [page, getDados]);

    if (loading)
        return <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />;

    function formatDate(date: any) {
        return format(formatUtcDate(date), 'dd-MM-yyyy', { locale: ptBR });
    };

    return (
        <div className="mt-2 space-y-2">
            <p className="flex w-full justify-center font-semibold my-4">{title}</p>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>ID</TableHead>
                        <TableHead>Processo</TableHead>
                        <TableHead>Executado</TableHead>
                        <TableHead>Tipo</TableHead>
                        <TableHead>Data Vencimento</TableHead>
                        <TableHead>Valor Parcela</TableHead>
                        <TableHead>Juros</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {loading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
                    {parcelamentoLis.map((parcelamento: any, i: number) => (
                        <>
                            <TableRow key={i}>
                                <TableCell>
                                    {parcelamento.id}
                                </TableCell>
                                <TableCell>
                                    {parcelamento.processo}
                                </TableCell>
                                <TableCell>
                                    {parcelamento.executado}
                                </TableCell>
                                <TableCell>
                                    {parcelamento.type == 1 ? 'Contrato' : 'Entrada'}
                                </TableCell>
                                <TableCell>
                                    {parcelamento.data && formatarData(parcelamento.data)}
                                    {/* {new Intl.DateTimeFormat('pt-BR').format(parseISO(parcelamento.data))} */}
                                </TableCell>
                                <TableCell>
                                    {
                                        new Intl.NumberFormat('pt-BR', {
                                            style: 'currency',
                                            currency: 'BRL'
                                        }).format(parcelamento.val_parcela ? parcelamento.val_parcela : 0)
                                    }
                                </TableCell>

                                <TableCell className="flex gap-1">
                                    {parcelamento.juros ? <CheckIcon className="h-4 w-4" /> : <Cross2Icon className="h-4 w-4" />}
                                </TableCell>
                            </TableRow>

                        </>
                    ))}
                </TableBody>
            </Table>
            <section>
                <PaginationActionsApi
                    itensPerPage={10}
                    count={total}
                    setPageIndex={setPage}
                    pageIndex={page}
                />
            </section>
            <section className="w-full">
                {success && (
                    <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
                )}
                {error && (
                    <AlertDestructive setError={setError}>{error}</AlertDestructive>
                )}
            </section>
        </div>
    );
}
