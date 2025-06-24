import { HotTable } from '@handsontable/react';
import { useState, useEffect } from 'react';
import axios from 'axios';

const SpreadsheetGrid = ({ spreadsheetId }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`/spreadsheets/${spreadsheetId}/data`).then(res => setData(res.data));
  }, [spreadsheetId]);

  return (
    <HotTable
      data={data}
      rowHeaders={true}
      colHeaders={true}
      licenseKey="non-commercial-and-evaluation"
    />
  );
};
export default SpreadsheetGrid;
