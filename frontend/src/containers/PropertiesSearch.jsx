import { TextSearchBox } from '../components/TextSearchBox';
import { useLazyGetPropertiesQuery } from '../servies_properties';
import { useState } from 'react';
import { ResultList } from '../components/Result';

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
    <div>
      <h1>Properties Search</h1>
      <TextSearchBox  onSubmit={submit}/> 
      <ResultList id={propertiesId}/>
    </div>
  );
}