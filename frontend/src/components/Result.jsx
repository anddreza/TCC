import { useGetPropertiesByIdQuery } from '../servies_properties';
import { Photos } from './Photos';

export const Field = (props) => {
    return (

        <div style={{ display: 'flex', gap: '2px' }}>
            <p>{props.label}</p>
            <p> {": "}</p>
            <p>{props.value}</p>
        </div>

    )
}


export const Result = (props) => {
    const result = useGetPropertiesByIdQuery(props.id);
    console.log("Result data:", result);
    const { data, isLoading } = result;
    if (isLoading || !data) return <div>Carregando...</div>;

    return (
        <div style={{ border: '1px solid #d1d5db', borderRadius: '8px', padding: '16px', backgroundColor: '#ffffff', marginBottom: '16px', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'flex', fontSize: '20px', fontWeight: '600' }}><p>{data.titulo}</p></div>
            <div style={{ flexDirection:'row', display:'flex', gap:'20px' }}>
                <div style={{flexDirection:'column', display: 'flex'}}>
                    <Photos photosList={data.fotos} />
                </div >
                <div style={{ flexDirection: 'column', display: 'flex'}}>
                    <Field label="Número de banheiros " value={data.numerobanhos} />
                    <Field label="Número de quartos" value={data.numeroquartos} />
                    <Field label="Número de vagas de garagem" value={data.numerovagas} />
                    <Field label="Área total m2 " value={data.areainterna} />
                    <Field label="Preço" value={data.valor} />
                    <a href={`https://www.itaivan.com/imovel/${data.url_amigavel}/${data.codigo}`}>Link para mais informações</a>

                </div>
            </div>
        </div>

    )
};

export const ResultList = (props) => {
    if (!props.id) return <div>No properties to display</div>

    return (
        <>
            {props.id.map((id) => <Result id={id} />)}

        </>
    )
};

