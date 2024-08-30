'use client';
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { useState } from "react";
import RltNegociacao from "./_components/RltNegociacao";
export default function Page() {
    const [rlt_negociacao, setRlt_negociacao] = useState<boolean>(false);
    const [rlt_outro, setRlt_Outro] = useState<boolean>(false);

    function carregarRlt(tipo: number) {
        //console.log(tipo);
        switch (tipo) {
            case 1:
                setRlt_negociacao(!rlt_negociacao);
                setRlt_Outro(false);
                break;
            case 2:
                setRlt_negociacao(false);
                setRlt_Outro(!rlt_outro);
                break;
        }
    }
    return (
        <Card className="shadow-2xl">
            <CardHeader>
                <CardTitle className="flex justify-center">Relatórios</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-rows-3 grid-flow-col gap-4">
                    <div className="row-auto w-56 border border-dotted">
                        <h1 className="font-semibold p-4">Selecione um Relatório</h1>
                        <Button
                            size={"lg"}
                            onClick={carregarRlt.bind(Number, 1)}
                            className="m-2 ml-6 w-44"
                        >
                            Negociações
                        </Button>
                        <Button
                            size={"lg"}
                            onClick={carregarRlt.bind(Number, 2)}
                            className="m-2 ml-6 w-44"
                        >
                            Outro
                        </Button>
                    </div>
                    <div className="row-span-3 col-span-12 border border-dotted">
                        <div className="m-2">
                            {rlt_negociacao && (
                                    <RltNegociacao />
                            )}
                        </div>
                    </div>
                </div>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>
    );
}