'use client'
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import {base64_image_logo, formatarData} from '@/lib/utils';
import { format } from "date-fns";

pdfMake.vfs = pdfFonts.pdfMake.vfs;

function generatePdfParcelamento(data, username) {
  try {
    //let dadosMultiplicados = Array(40).fill(dados).flat();

    const content = data.map((item) => {
      return [
        { text: item.id, fontSize: 8 },
        { text: item.numero_parcela, fontSize: 8 },
        { text: item.processo, fontSize: 8 },
        {
          text: item.executado,
          fontSize: 8,
        },
        { text: item.type==1 ? 'Contrato' : 'Entrada', fontSize: 8, alignment: "center" },
        { text: item.data && formatarData(item.data), fontSize: 8, alignment: "center" },
        { text: item.val_parcela ? new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
          }).format(item.val_parcela): '',
          fontSize: 8, alignment: "right" },
        { text: item.val_pago ? new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
          }).format(item.val_pago): '', fontSize: 8, alignment: "right" },
        { text: item.data_pgto && formatarData(item.data_pgto), fontSize: 8, alignment: "center" },
        {
          text: item.is_val_juros ? "S" : "N",
          fontSize: 8,
          alignment: "center",
        },
      ];
    });

    // Define uma função para calcular o total do campo field3
    const totalField3 = data.reduce(
      (acc, item) => acc + parseFloat(item.val_pago),
      0
    );

    // Formatar a data e a hora
    const dataFormatada = format(new Date(), "dd/MM/yyyy");
    const horaFormatada = format(new Date(), "HH:mm");

    // Define a estrutura do cabeçalho com a imagem e o texto
    const header = {
      columns: [
        {
          image: base64_image_logo,
          width: 200, // Largura da imagem
          margin: [40, 10, 0, 0], // Margem superior
        },
      ],
      //marginTop: 10,
    };

    // Define a estrutura do documento PDF
    const docDefinition = {
      pageSize: "A4",
      pageOrientation: "landscape",
      header: function (currentPage) {
        if (currentPage === 1) {
          return header;
        }
        return null; // Retorna null para ocultar o cabeçalho nas páginas subsequentes
      },
      footer: function (currentPage, pageCount) {
        return {
          text: `Usuario:${username+" ".repeat(
            50
          )} ${dataFormatada} às ${horaFormatada}${" ".repeat(
            50
          )} Página ${currentPage.toString()} de ${pageCount}`,
          alignment: "right",
          margin: [0, 0, 20, 0],
          fontSize: 7,
        };
      },
      content: [
        {
          text: "RELATÓRIO DE NEGOCIAÇÃO POR PERÍODO",
          alignment: "center",
          margin: [0, 50, 0, 0], // Margem superior
          overflow: "visible",
          fontSize: 12,
          bold: true,
        },
        {
          table: {
            widths: [
              30,
              30,
              105,
              300,
              "auto",
              "auto",
              "auto",
              "auto",
              "auto",
              "auto",
            ],
            body: [
              [
                {
                  text: "ID",
                  fontSize: 10,
                  fillColor: "#bbf7d0",
                  alignment: "center",
                },
                {
                  text: "PARC",
                  fontSize: 10,
                  fillColor: "#bbf7d0",
                  alignment: "center",
                },
                {
                  text: "PROCESSO",
                  fontSize: 10,
                  fillColor: "#bbf7d0",
                  alignment: "center",
                },
                {
                  text: "EXECUTADO",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "TIPO",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "DATA",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "VALOR PARCELA",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "VALOR PAGO",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "DATA PGTO",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
                {
                  text: "É JUROS",
                  fontSize: 10,
                  alignment: "center",
                  fillColor: "#bbf7d0",
                },
              ], // Cabeçalho da tabela
              ...content, // Conteúdo da tabela
            ],
            overflow: "visible",
          },
          marginTop: 10, // Margem superior do conteúdo
          layout: {
            // Configurações do layout para cada página
            fillColor: function (i, node) {
              return i === 0 ? null : i % 2 === 0 ? "#CCCCCC" : null;
            }, // Define uma cor de fundo alternada para as linhas da tabela
            marginTop: 50,
          },
        },
        // Seção separada para exibir o total
        {
          text: `Total Valor Recebido: ${
            !Number.isNaN(totalField3) ? totalField3.toFixed(2) : 0
          }`,
          margin: [0, 20, 0, 0], // Margem superior
          fontSize: 9,
        },
      ],
    };

    // Gera o PDF
    pdfMake.createPdf(docDefinition).open();
  } catch (error) {
    console.error("Erro ao gerar o PDF:", error);
  }
}

export default generatePdfParcelamento;
