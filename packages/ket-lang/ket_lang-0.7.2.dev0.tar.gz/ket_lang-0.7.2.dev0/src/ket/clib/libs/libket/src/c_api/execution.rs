// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2024 2024 Otávio Augusto de Santana Jatobá <otavio.jatoba@grad.ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Debug, Clone)]
pub struct BatchCExecution {
    submit_execution: fn(*const u8, usize),
    get_result: fn(data: &mut *const u8, len: &mut usize),
    get_status: fn() -> u8,
}

impl crate::BatchExecution for BatchCExecution {
    fn submit_execution(&mut self, instructions: &[crate::Instruction]) {
        let instructions = serde_json::to_vec(instructions).unwrap();
        (self.submit_execution)(instructions.as_ptr(), instructions.len());
    }

    fn get_result(&mut self) -> crate::ResultData {
        let mut buffer = std::ptr::null();
        let mut len: usize = 0;
        (self.get_result)(&mut buffer, &mut len);
        let buffer = unsafe { std::slice::from_raw_parts(buffer, len) };
        serde_json::from_slice(buffer).unwrap()
    }

    fn get_status(&self) -> crate::ExecutionStatus {
        match (self.get_status)() {
            0 => crate::ExecutionStatus::New,
            1 => crate::ExecutionStatus::Ready,
            2 => crate::ExecutionStatus::Running,
            3 => crate::ExecutionStatus::Completed,
            _ => crate::ExecutionStatus::Error,
        }
    }
}

#[no_mangle]
pub extern "C" fn ket_batch_make_configuration(
    num_qubits: usize,
    batch: &BatchCExecution,
    result: &mut *mut crate::Configuration,
) -> i32 {
    let batch = Box::new(batch.clone());

    *result = Box::into_raw(Box::new(crate::Configuration {
        allow_measure: true,
        allow_sample: true,
        allow_exp_value: true,
        allow_dump: false,
        valid_after_measure: false,
        continue_after_sample: false,
        continue_after_exp_value: false,
        continue_after_dump: false,
        decompose: false,
        live_quantum_execution: None,
        batch_execution: Some(batch),
        num_qubits,
        execution_timeout: None,
    }));

    0
}
