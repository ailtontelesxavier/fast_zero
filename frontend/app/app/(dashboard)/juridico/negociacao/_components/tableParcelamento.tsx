'use client';

import { AlertDestructive } from "@/components/AlertDestructive";
import { AlertSuccess } from "@/components/AlertSuccess";
import { Icons } from "@/components/icons";
import { PaginationActionsApi } from "@/components/paginationActionsApi";
import { format, parseISO } from "date-fns";
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
import { Button } from "@/components/ui/button";
import FormParcela from "./formParcela";
import AlertDialogComp from "@/components/AlertDialog";
export default function TableParcelamento({ type, negociacao_id }: { type: 1 | 2, negociacao_id: number }) {
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState<number>(1);
    const [loading, setLoading] = useState(false);
    const [isBusca, setIsBusca] = useState(true);
    const [parcelamentoLis, setParcelamentoList] = useState([]);

    useEffect(() => {

        if (negociacao_id > 0 && isBusca) obterParcelamentoList();

        setIsBusca(false)
        async function obterParcelamentoList() {
            try {
                setLoading(true);
                await api
                    .get(`/juridico/parcelamento?negociacao_id=${negociacao_id}&type=${type}&page=${page}&page_size=10`)
                    .then((response) => {
                        setParcelamentoList(response.data.rows);
                        setTotal(response.data.total_records);
                    }).catch((error) => {
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

    }, [page, negociacao_id, type, isBusca])

    function formatDate(date: any) {
        return format(formatUtcDate(date), 'dd-MM-yyyy', { locale: ptBR });
    };

    function setPageN(numero: number){
        setIsBusca(true);
        setPage(numero);
    }

    return (
        <div className="mt-2 space-y-2">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>ID</TableHead>
                        <TableHead>Parcela</TableHead>
                        <TableHead>Data</TableHead>
                        <TableHead>Valor Parcela</TableHead>
                        <TableHead>Valor Pago</TableHead>
                        <TableHead>Pagamento</TableHead>
                        <TableHead>Juros</TableHead>
                        <TableHead>Ações</TableHead>
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
                                    {parcelamento.numero_parcela}
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
                                <TableCell>
                                    {
                                        new Intl.NumberFormat('pt-BR', {
                                            style: 'currency',
                                            currency: 'BRL'
                                        }).format(parcelamento.val_pago ? parcelamento.val_pago : 0)
                                    }
                                </TableCell>
                                <TableCell>
                                    {parcelamento.data_pgto && formatarData(parcelamento.data_pgto)}
                                </TableCell>
                                <TableCell>
                                    {parcelamento.is_val_juros}
                                </TableCell>
                                <TableCell className="flex gap-1">
                                    <FormParcela id={parcelamento.id} negociacao_id={negociacao_id} setIsBusca={setIsBusca} />
                                    <AlertDialogComp
                                        title="Tem certeza que deseja excluir?"
                                        description=""
                                        param={parcelamento}
                                        acao={deleteParcela}
                                    />
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
                    setPageIndex={setPageN}
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

    async function deleteParcela(obj: any) {
        try {
            //console.log(obj.id)
            await api
                .delete(`/juridico/parcelamento/${obj.id}`)
                .then((response: any) => {
                    if (response.status === 200) {
                        setSuccess("Excluido com sucesso");
                        setIsBusca(true);
                    }
                }).catch((error) => {
                    const responseObject = JSON.parse(error.request.response)
                    var errors = ''
                    responseObject.detail.forEach((val: any) => {
                        errors += (`(Campo: ${val.loc[1]} Erro: ${val.msg}) `)
                    });
                    setError("Error interno: " + errors)
                });
        } catch (error: any) {
            if (error.response) {
                setError(error.response.data.detail + "; " + error.message);
            }
        }
    }
}