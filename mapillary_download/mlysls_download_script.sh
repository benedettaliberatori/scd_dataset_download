#!/bin/bash

declare -A files=(
    ["msls_images_vol_1.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An-x6BOZeUDmFXVxCKtosZWgMZzQiLR1iBxkevoDhNKLyXwMULUhqUB5pExN3EDE7RfPewnC6_Omad8kkRV1vwyOhWXqOJp3-3d6hWARSf_41taXCsAlVF1gp5gf2S7W.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=Adm7MsGvI1FZL87ngudLrmwC_FC5X_ma7N-Nu9X3W2sN2KFH_OOonFwosRtMICKWvio&ccb=10-5&oh=00_AfqpiNyjRlZn175bMgFHNV8VV0MM8vwh8JdR4E9om8wYXg&oe=698F13D1&_nc_sid=6de079"
    ["msls_images_vol_2.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An9l_yexUWNWbUOGWt-7HVC-ONHffIDJQeVnpo4Fp3-X7p6f7NoevyddUQ4WdsoufwUjzW2nhB29AMgdRm8WSxAup2B6qZikAC4tGtMaC0x3PLJn76tkBpMhjqlb_lLs.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=AdnzyJeNg_-fDBdlzwmtl_wvidnWV-WmkbwRqBjDoU78kuiqLTsAgqJNSgb1okgeEh0&ccb=10-5&oh=00_Afqlj7GS1aQ7eSBOSBCosrJkhHykbxSfwOD5FlveocfJrg&oe=698EECB7&_nc_sid=6de079"
    ["msls_images_vol_3.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An-McnhyZtsCZK-zzwCIPBlWXhBl4d3Qas_TyqLiRHb8VvEP_ilvcJftXCAcmvirTo1NBF_EJKzEgSdrFu0owLWvywQ4S7y6GNpFYb7XxokmgVpeGlisqVTWkOE4Wi9P.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=Adl4jtElJfHimGhSQwW1LtlYw-l-qTxk5z_983PTlzsWKH41S-wT-qfDkJSCyYDjsKw&ccb=10-5&oh=00_AfrlzptcHmRALA_A5lsimVypV5SvxLOHaWPaFFZole4zMw&oe=698F156E&_nc_sid=6de079"
    ["msls_images_vol_4.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An8vpu-mDXBO2YvVoOO9wcXuIVUF_6yTrxKFB4Wp4tFjaVnRcEqlmvTTdFk-lxjv0VVGFoowHUXsCUuUiykQ8d7dKaLx6Atvtw07uLfPbDhTrpoWdlA-FasNCMKuxCvp.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=AdnnC3j8qugx3PMbij9EIQV9DhnSUlJKIaMAJhKFntf7sHFThkXrE2fL7ZbTuFtJocQ&ccb=10-5&oh=00_AfrYn47ViMUxhCyfVpGLci_XBMSy9ICZVB_tvgFwNcJ47Q&oe=698F0E2B&_nc_sid=6de079"
    ["msls_images_vol_5.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An9e0HGaRi-9kM8QyF5wNHyA-DVxI_C_aN9rC3iAXHLN9_RoW9P8SUHRR39AeszPqegQnqk-LL49sYIjsAIdS23yl9rwu1NPOdDbjFmvzlTYERwsxv6nAObVUBNOjDrN.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=AdmAlwrK8vghQX3oDvdN-cUA0kGxh_5Clz4SDxtxh4P2-TytTpPLJWFg5Fqo0MGUcag&ccb=10-5&oh=00_AfpzCnXJB4-MR335GEjqb7LVELjCEij8IMAHXhWw1Zb82w&oe=698F163E&_nc_sid=6de079"
    ["msls_images_vol_6.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An-zh-eec0DwQv9bkj0KVhowIEpbMW6qg578XP4PU51TH-5PpQtKYJDb8kax3KBOn1qXKeM9jUsKeaqkaEIxqpZFfsJ6tITsg2jsz7Wd9mSTWSLR3EuyXcjLzBGDImv_.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=AdnvbX0md46uTRmoxK7W8SFwLqULt9KL5ZepM9JABhOMDsB1Hk6d76-BsZZ_CShAO0o&ccb=10-5&oh=00_AfpbwfR2mJMlGiLNjun-y-Qp-NqRANrxN75_FD0LGUdWMA&oe=698F0A21&_nc_sid=6de079"
    ["msls_metadata.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An9znN6Evsbp2KNZvdYc0NsYCk961Vy0u_j6ACpZ_QoylW800rBKCSeZQAq765BP03K_qyPpPK8aCNU6wnVa44M6cmx4X-iTJVQ8zCwaH5BJom47I8Xr25XLTw.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=AdlRInM4oWZJWI9pyliD1lff5bxWqRPnqdMFlqDQQbz4w_9Q2Pyn0eNsSbnHevhTF5o&ccb=10-5&oh=00_AfqsOEHfqcgzcKIPJcIF0lDVX8Ersb05WFeT99sKMOudUg&oe=698EF758&_nc_sid=6de079"
    ["msls_patch_v1.1.zip"]="https://scontent-cdg4-3.xx.fbcdn.net/m1/v/t6/An9DCNVm9dpPbX3zG544xA35U2Qqb7oPWrN3-_39Fp9NxF2oKLx3cKw3QKzPL5bsNokN-NodhGD-mHrUZsXVfA3Zil71HcjIZXJ3Lk8P5jktf3sftUlmO_9sohJb.zip?_nc_gid=DgfS2hNUc6vQBFPRXe_sQA&_nc_oc=Adn_4SeYj9IUSxWR-U_WVDnx3WIUGW1Q0lfShdMHFUzF5l0WglDUoFT_jDviA631Feo&ccb=10-5&oh=00_AfrFPvoUTELbyvS_KHhauoULBZC1mbKzkAsaeosJzApi3A&oe=698F1872&_nc_sid=6de079"
)

for filename in "${!files[@]}"; do
    url="${files[$filename]}"
    
    echo "-----------------------------------------------"
    
    if curl -fsSL -o "$filename" "$url"; then
        echo "Download successful. Unzipping $filename..."
        
        if unzip -oq "$filename"; then
            echo "Successfully unzipped $filename."
        else
            echo "FAILED to unzip $filename."
        fi
    else
        echo "FAILED to download $filename. (Link might be expired)"
    fi
done

echo "-----------------------------------------------"
echo "All tasks finished."