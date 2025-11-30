import { TextSearchBox } from '../components/TextSearchBox';
import { useLazyGetPropertiesQuery } from '../servies_properties';
import { useState } from 'react';
import { ResultList } from '../components/Result';
import { HomeOutlined } from '@ant-design/icons';

export const PropertiesSearch = () => {
  //to call endpoint until the use click on 'submit'
  const [getProperties] = useLazyGetPropertiesQuery();
  //state to hold the list of property IDs
  const [propertiesId, setPropertiesId] = useState([]);

  const submit = async (value) => {
    const result = await getProperties(value);
    setPropertiesId(result.data.ids);
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      alignItems: 'center',
      paddingTop: '100px',
      width: '100%', 
      minHeight: '100vh',
      backgroundColor: '#f0f2f5',
    }}>
      <HomeOutlined style={{ fontSize: '50px' }} />
      <h1>Assistente de Imóveis</h1>

      <TextSearchBox onSubmit={submit} />
      <ResultList id={propertiesId} />
    </div>
  );
}