"use client";

import { CardContent } from "@/components/CardContent";
import PageTitle from "@/components/PageTitle";
import api from "@/lib/api";
import { useEffect, useState } from "react";
import AlertDialogComp from "@/components/AlertDialog";
import { AlertSuccess } from "@/components/AlertSuccess";
import { AlertDestructive } from "@/components/AlertDestructive";
import FormModule from "../_components/FormModule";

export default function PermissonView() {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [modules, setModules] = useState<any>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState<number>(1);
  const [isBusca, setIsBusca] = useState(true);

  useEffect(() => {
    if (isBusca) obterModules();

    setIsBusca(false);

    async function obterModules() {
      await api
        .get(`/permissoes/module/?page=${page}&page_size=10`)
        .then((response) => {
          setModules(response.data.modules);
          setTotal(response.data.total_records);
        });
    }
  }, [page, isBusca]);

  async function deleteModule(id: number) {
    try {
      await api
        .delete("/permissoes/module/" + id)
        .then((response: any) => {
          if (response.status === 200) {
            setSuccess("Excluido com sucesso");
            setIsBusca(true);
          }
        })
        .catch((error) => setError("Error interno: " + error));
    } catch (error: any) {
      if (error.response) {
        setError(error.response.data.detail + "; " + error.message);
      }
    }
  }

  return (
    <div className="grid w-full">
      <PageTitle title="Gestao de Permissao" />
      <section className="mt-3 transition-all p-2 rounded-md w-1/2">
        <CardContent className="min-w-96">
          <div className="flex flex-row justify-between">
            <h3>Modulo</h3>
            <div>
              <FormModule setIsBusca={setIsBusca} id={0} />
            </div>
          </div>
          <table className="hidden md:block w-full">
            <thead className="bg-gray-50 border-b-2 border-gray-200">
              <tr>
                <th className="w-20 p-3 text-sm font-semibold tracking-wide text-left">
                  ID
                </th>
                <th className="p-3 text-sm font-semibold tracking-wide text-left">
                  NOME
                </th>
                <th className="p-3 text-sm font-semibold tracking-wide text-left"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {modules.map((module: any, i: number) => (
                <>
                  {i % 2 === 0 ? (
                    <tr key={i} className="bg-white">
                      <td className="p-3 text-sm text-gray-700 hover:cursor-pointer whitespace-nowrap">
                        <span className="font-bold text-blue-500 ">
                          {module.id}
                        </span>
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        {module.title}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        <div className="flex gap-2">
                          <FormModule setIsBusca={setIsBusca} id={module.id} />
                          <AlertDialogComp
                            title="Tem certeza que deseja excluir?"
                            description=""
                            param={module.id}
                            acao={deleteModule}
                          />
                        </div>
                      </td>
                    </tr>
                  ) : (
                    <tr key={i} className="bg-gray-50">
                      <td className="p-3 text-sm text-gray-700 hover:cursor-pointer whitespace-nowrap">
                        <span className="font-bold text-blue-500 hover:underline">
                          {module.id}
                        </span>
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        {module.title}
                      </td>
                      <td className="p-3 text-sm text-gray-700 whitespace-nowrap">
                        <div className="flex gap-2">
                          <FormModule setIsBusca={setIsBusca} id={module.id} />
                          <AlertDialogComp
                            title="Tem certeza que deseja excluir?"
                            description=""
                            param={module.id}
                            acao={deleteModule}
                          />
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden">
            {modules &&
              modules.map((data: any) => (
                <>
                  <div className="bg-white space-y-3 p-4 rounded-lg shadow">
                    <div className="flex items-center space-x-2 text-sm">
                      <div>
                        <a
                          href="#"
                          className="text-blue-500 font-bold hover:underline"
                        >
                          {data.id}
                        </a>
                      </div>
                    </div>
                    <div className="text-sm text-gray-700">{data.title}</div>
                    <div className="flex gap-2">
                      <FormModule setIsBusca={setIsBusca} id={data.id} />
                      <AlertDialogComp
                        title="Tem certeza que deseja excluir?"
                        description=""
                        param={data.id}
                        acao={deleteModule}
                      />
                    </div>
                  </div>
                </>
              ))}
          </div>
          <section className="w-full">
            {success && (
              <AlertSuccess setSuccess={setSuccess}>{success}</AlertSuccess>
            )}
            {error && (
              <AlertDestructive setError={setError}>{error}</AlertDestructive>
            )}
          </section>
        </CardContent>
      </section>
    </div>
  );
}
