import { TextSearchBox } from '../components/TextSearchBox';
import { useLazyGetPropertiesQuery } from '../servies_properties';
import { useState } from 'react';
import { ResultList } from '../components/Result';
import { HomeOutlined } from '@ant-design/icons';

export const PropertiesSearch = () => {
  const [getProperties] = useLazyGetPropertiesQuery();
  const [propertiesId, setPropertiesId] = useState(["68d03e0f1f6b16923112cc1c", "68d03e0f1f6b16923112cc1d"]);

  const submit = async (value) => {
    console.log('Search submitted with value:', value);
    const result = await getProperties(value);
    console.log('Properties fetched:', result);
    setPropertiesId(result.data.ids);
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      alignItems: 'center',
      height: '100vh',
      paddingTop: '100px',
      width: '100%'
    }}>
      <HomeOutlined style={{ fontSize: '50px' }} />
      <h1>Assistente de Imóveis</h1>

      <TextSearchBox onSubmit={submit} />
      <ResultList id={propertiesId} />
    </div>
  );
}