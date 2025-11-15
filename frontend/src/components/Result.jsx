import { Card } from 'antd';
import { useGetPropertiesByIdQuery } from '../servies_properties';

export const Result = (props) => {
    const result  = useGetPropertiesByIdQuery(props.id);
    console.log("Result data:", result);
    const { data, isLoading } = result;
    if (isLoading) return <div>Carregando...</div>;

    return (

        <Card 
        title={data.titulo} 
        cover={<img  draggable={false} 
        src={data.fotos[0].url}/>} 
        
        style={{ width: 300 }}>
            <p></p>
        </Card>
        
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
