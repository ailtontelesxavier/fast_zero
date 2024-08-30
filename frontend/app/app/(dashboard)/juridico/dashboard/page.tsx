'use client';
import api from "@/lib/api";
import { TableResumoNegociacaoVenc } from "./_components/TableResumoNegociacaoVenc";
import { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import CardResumoNegociacao from "./_components/CardResumoNegociacao";


export default function Dashboard() {
    const [render_table, setRender_table] = useState<Number | null>(null);
    async function onSubmit(data: any) {
        console.log(data)

        switch (data) {
            case 1:
                setRender_table(render_table ? null : 1);
                break;
            case 2:
                setRender_table(render_table ? null : 2);
                break;
            case 3:
                setRender_table(render_table ? null : 3);
                break;
            default:
                setRender_table(null);
                break;
        }
    }

    useEffect(()=>{

    },[render_table])

    return (
        <>
            <Card className="w-full min-h-screen rounded shadow-2xl ">
                <CardHeader>
                    <CardTitle className="flex justify-center">
                        Jurídico - Dashboard
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                        <CardResumoNegociacao title={'Parcelamentos Vencidos'} getDados={getNegociacaoVenciados} onClick={onSubmit.bind(Number, 1)} />
                        <CardResumoNegociacao title={'Há venc. na Semana'} getDados={getNegociacaoVenciNaSemana} onClick={onSubmit.bind(Number, 2)} />
                        <CardResumoNegociacao title={'Há Venc. prox. 30 dias'} getDados={getNegociacaoHaVenc30d} onClick={onSubmit.bind(Number, 3)} />
                    </div>
                    <div className="gap-4 mt-10">
                        {render_table === 1 && <TableResumoNegociacaoVenc title={'Parcelamentos Vencidos'} getDados={getNegociacaoVenciados} />}
                        {render_table === 2 && <TableResumoNegociacaoVenc title={'Há venc. na Semana'} getDados={getNegociacaoVenciNaSemana} />}
                        {render_table === 3 && <TableResumoNegociacaoVenc title={'Há Venc. prox. 30 dias'} getDados={getNegociacaoHaVenc30d} />}
                    </div>
                </CardContent>
                <CardFooter className="flex justify-between"></CardFooter>
            </Card>
        </>);

    async function getNegociacaoVenciNaSemana(page: number) {
        return await api.get(`/juridico/negociacao/relatorio/venci-na-semana?page=${page}&page_size=10`)

    }
    async function getNegociacaoHaVenc30d(page: number) {
        return await api.get(`/juridico/negociacao/relatorio/ha-venc-30d?page=${page}&page_size=10`)

    }
    async function getNegociacaoVenciados(page: number) {
        return await api.get(`/juridico/negociacao/relatorio/negoc-venvidos?page=${page}&page_size=10`)
    }
}