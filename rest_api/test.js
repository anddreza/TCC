// Cypress.Commmands.add('CrateDispositivo', async (deviceData = {}) => {
//     function getToken(){
//        return cy.request({
//             method: 'POST',
//             url: 'http://localhost:3000/authenticate',
//             body: {
//                 username: 'admin',
//                 password: 'admin',
//             },
//         }).then((response) => {
//             return response.body.token; 
//         })
//     }

//     cy.fixture('Computadores.json').then(computadores) => {
//             const body ={
//                 ...computadores,
//                 ...deviceData
//             }

//     {
//         computadorC: {
//             deviceInfo: {
//                 serialNumber: "1",
//                 unifiqueIdentifier: "",
//             }
//         }
//     }
     
//     body.computadorC.deviceInfo.serialNumber = getRandomIntInclusive(1, 100) //????
//     body.computadorC.deviceInfo.unifiqueIdentifier = alterarUnifique()

    
//     const token = await getToken()
//         const response = await cy.request({
//             method: 'POST',
//             url: 'http://localhost:3000/dispositivos',
//             headers: {
//                 Authorization: `Bearer ${token}`,
//                 'AGENT-TOKEN': 'TESTE1234',
//             },
//             body: deviceData,
//         })
//         expect(response.status).to.eq(201);
//     }
// });